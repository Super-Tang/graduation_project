import sentencepiece as spm
import sentence_alignment.Globals as Globals


def process_file(source_text, target_text, language, args):
    sp = spm.SentencePieceProcessor()
    # print(source_text)
    # print(target_text)
    if language == Globals.ENGLISH:
        sp.Load(args.en_bpe_model_dir)
    elif language == Globals.FRENCH:
        sp.load(args.fr_bpe_model_dir)
    elif language == Globals.RUSSIAN:
        sp.load(args.ru_bpe_model_dir)
    elif language == Globals.GERMAN:
        sp.load(args.de_bpe_model_dir)
    elif language == Globals.SPAIN:
        sp.load(args.es_bpe_model_dir)
    fout = open(args.predict_file, 'w', encoding='utf-8')
    sentence_count = len(source_text)
    for i in range(sentence_count):
        line1 = source_text[i]
        line2 = target_text[i]
        pieces1 = sp.EncodeAsPieces(line1.strip())
        pieces2 = sp.EncodeAsPieces(line2.strip())
        fout.write(" ".join(pieces2) + "\t" + " ".join(pieces1) + '\n')
    fout.close()
