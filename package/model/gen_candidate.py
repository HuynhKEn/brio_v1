import os
import sys
import torch
import argparse
from typing import List
from model import RankingLoss, BRIO
from model_pho import RankingLoss, BRIO
from transformers import MBartForConditionalGeneration, BartForConditionalGeneration, AutoTokenizer, BartTokenizer, PegasusTokenizer, PegasusForConditionalGeneration

def generate_summaries_cnndm(args):
    device = f"cuda:{args.gpuid}"
    #mname = "facebook/bart-large-cnn"
    mname = "./bartpho2"
    tokenizer = AutoTokenizer.from_pretrained(mname)
    #model = BartForConditionalGeneration.from_pretrained(mname).to(device)
    #model = MBartForConditionalGeneration.from_pretrained(mname).to(device)
    model = BRIO("./bartpho2", tokenizer.pad_token_id, False)
    model.load_state_dict(torch.load(os.path.join("./cache", "23-08-03-0/model_generation.bin"), map_location=f'cuda:{args.gpuid[0]}')) #Uncomment this line when you already trained a BRIO model
    model.eval();  model.generation_mode()
    max_length = 140; min_length = 55; count = 1; bsz = 1
    with open(args.src_dir, encoding="utf-8") as source, open(args.tgt_dir, 'w', encoding="utf-8") as fout:
        sline = source.readline().strip().lower()
        slines = [sline]
        for sline in source:
            if count % 100 == 0:
                print(count, flush=True)
            if count % bsz == 0:
                with torch.no_grad():
                    dct = tokenizer.batch_encode_plus(slines, max_length=1024, return_tensors="pt", pad_to_max_length=True, truncation=True)
                    summaries = model.generate(
                        input_ids=dct["input_ids"].to(device),
                        attention_mask=dct["attention_mask"].to(device),
                        num_return_sequences=6, num_beam_groups=6, diversity_penalty=1.0, num_beams=6,
                        max_length=max_length + 2,  # +2 from original because we start at step=1 and stop before max_length
                        min_length=min_length + 1,  # +1 from original because we start at step=1
                        no_repeat_ngram_size=3,
                        length_penalty=2.0,
                        early_stopping=True,
                    )
                    dec = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summaries]
                for hypothesis in dec:
                    hypothesis = hypothesis.replace("\n", " ")
                    fout.write(hypothesis + '\n')
                    fout.flush()
                slines = []
            sline = sline.strip().lower()
            if len(sline) == 0:
                sline = " "
            slines.append(sline)
            count += 1
        if slines != []:
            with torch.no_grad():
                dct = tokenizer.batch_encode_plus(slines, max_length=1024, return_tensors="pt", pad_to_max_length=True, truncation=True)
                summaries = model.generate(
                    input_ids=dct["input_ids"].to(device),
                    attention_mask=dct["attention_mask"].to(device),
                    num_return_sequences=6, num_beam_groups=6, diversity_penalty=1.0, num_beams=6,
                    max_length=max_length + 2,  # +2 from original because we start at step=1 and stop before max_length
                    min_length=min_length + 1,  # +1 from original because we start at step=1
                    no_repeat_ngram_size=3,
                    length_penalty=2.0,
                    early_stopping=True,
                )
                dec = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summaries]
            for hypothesis in dec:
                    hypothesis = hypothesis.replace("\n", " ")
                    fout.write(hypothesis + '\n')
                    fout.flush()


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser(description='Parameters')
    parser.add_argument("--gpuid", type=int, default=0, help="gpu id")
    parser.add_argument("--src_dir", type=str, help="source file")
    parser.add_argument("--tgt_dir", type=str, help="target file")
    parser.add_argument("--dataset", type=str, default="cnndm", help="dataset")
    args = parser.parse_args()
    if args.dataset == "cnndm":
        generate_summaries_cnndm(args)