import os
import threading

import numpy as np
import paddle.fluid as fluid

# include task-specific libs
import phrase_alignment.desc as desc
import phrase_alignment.reader as reader
# include palm for easier nlp coding
from phrase_alignment.palm.toolkit.input_field import InputField
from phrase_alignment.transformer import create_net, position_encoding_init


def init_from_pretrain_model(args, exe, program):

    assert isinstance(args.init_from_pretrain_model, str)

    if not os.path.exists(args.init_from_pretrain_model):
        raise Warning("The pretrained params do not exist.")
        return False

    def existed_params(var):
        if not isinstance(var, fluid.framework.Parameter):
            return False
        return os.path.exists(
            os.path.join(args.init_from_pretrain_model, var.name))

    fluid.io.load_vars(
        exe,
        args.init_from_pretrain_model,
        main_program=program,
        predicate=existed_params)

    print("finish initing model from pretrained params from %s" %
          (args.init_from_pretrain_model))

    return True


def init_from_params(args, exe, program):

    assert isinstance(args.init_from_params, str)

    if not os.path.exists(args.init_from_params):
        raise Warning("the params path does not exist.")
        return False

    fluid.io.load_params(
        executor=exe,
        dirname=args.init_from_params,
        main_program=program,
        filename="params.pdparams")

    print("finish init model from params from %s" % (args.init_from_params))

    return True


def post_process_seq(seq, bos_idx, eos_idx, output_bos=False, output_eos=False):
    """
    Post-process the beam-search decoded sequence. Truncate from the first
    <eos> and remove the <bos> and <eos> tokens currently.
    """
    eos_pos = len(seq) - 1
    for i, idx in enumerate(seq):
        if idx == eos_idx:
            eos_pos = i
            break
    seq = [
        idx for idx in seq[:eos_pos + 1]
        if (output_bos or idx != bos_idx) and (output_eos or idx != eos_idx)
    ]
    return seq


class Predict_thread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.args = args
        self.weights = []
        self.done = False
        self.end_message = None
        if args.use_cuda:
            dev_count = fluid.core.get_cuda_device_count()
            place = fluid.CUDAPlace(0)
        else:
            dev_count = int(os.environ.get('CPU_NUM', 1))
            place = fluid.CPUPlace()
    # define the data generator
        processor = reader.DataProcessor(
        fpattern=args.predict_file,
        src_vocab_fpath=args.src_vocab_fpath,
        trg_vocab_fpath=args.trg_vocab_fpath,
        token_delimiter=args.token_delimiter,
        use_token_batch=False,
        batch_size=args.batch_size,
        device_count=dev_count,
        pool_size=args.pool_size,
        sort_type=reader.SortType.NONE,
        shuffle=False,
        shuffle_batch=False,
        start_mark=args.special_token[0],
        end_mark=args.special_token[1],
        unk_mark=args.special_token[2],
        max_length=args.max_length,
        n_head=args.n_head)
        self.batch_generator = processor.data_generator(phase="train")
        args.src_vocab_size, args.trg_vocab_size, args.bos_idx, args.eos_idx, \
            args.unk_idx = processor.get_vocab_summary()
        trg_idx2word = reader.DataProcessor.load_dict(
            dict_path=args.trg_vocab_fpath, reverse=True)

        test_prog = fluid.default_main_program()
        startup_prog = fluid.default_startup_program()

        with fluid.program_guard(test_prog, startup_prog):
            with fluid.unique_name.guard():
                input_field_names = desc.encoder_data_input_fields + \
                    desc.decoder_data_input_fields[:-1] + desc.label_data_input_fields
                input_slots = [{
                "name": name,
                "shape": desc.input_descs[name][0],
                "dtype": desc.input_descs[name][1]
                    } for name in input_field_names]

                self.input_field = InputField(input_slots)
                self.input_field.build(build_pyreader=True)

            # define the network
        
                self.weight_matrix = create_net(
                    is_training=False, model_input=self.input_field, args=args)

                # self.weight_matrix.persistable = True
    # This is used here to set dropout to the test mode.
        self.test_prog = test_prog.clone(for_test=True)

    # prepare predicting

    ## define the executor and program for training

        self.exe = fluid.Executor(place)

        self.exe.run(startup_prog)
        assert (args.init_from_params)

        init_from_params(args, self.exe, self.test_prog)



    # to avoid a longer length than training, reset the size of position encoding to max_length
        for pos_enc_param_name in desc.pos_enc_param_names:
            pos_enc_param = fluid.global_scope().find_var(
            pos_enc_param_name).get_tensor()

            pos_enc_param.set(
            position_encoding_init(args.max_length + 1, args.d_model), place)

        exe_strategy = fluid.ExecutionStrategy()
    # to clear tensor array after each iteration
        exe_strategy.num_iteration_per_drop_scope = 1
        compiled_test_prog = fluid.CompiledProgram(self.test_prog).with_data_parallel(
        exec_strategy=exe_strategy, places=place)

    def run(self):
        self.input_field.reader.decorate_batch_generator(self.batch_generator)
        self.input_field.reader.start()
        count = 0
        while True:
            count += 1
            try:
                weight_matrix = self.exe.run(
                    self.test_prog,
                    fetch_list=[self.weight_matrix],return_numpy=False)
                eight_weight = np.array(weight_matrix[0])[0]
                predict_weight = eight_weight[0]
                for i in range(len(eight_weight)):
                    if i > 0:
                        predict_weight += eight_weight[i]
                self.weights.append((count, predict_weight))
            except fluid.core.EOFException:
                self.end_message = 'Process finished!'
                self.done = True
                break


