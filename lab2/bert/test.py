import torch
from wordsegment import WordSegmenter
from transformers import AutoModelForTokenClassification,BertTokenizerFast

model_name = "ckiplab/bert-base-chinese-ws"
model = AutoModelForTokenClassification.from_pretrained(model_name)
tokenizer = BertTokenizerFast.from_pretrained(model_name)
ws = WordSegmenter(model=model,tokenizer=tokenizer,device = torch.device("cuda" if torch.cuda.is_available() else "cpu"))
sentence = ["人生的缺憾，最大的就是和别人比较，和高人比较使我们自卑；和俗人比较，使我们下流；和下人比较，使我们骄满。外来的比较是我们心灵动荡不能自在的来源，也是的大部分的人都迷失了自我，障蔽了自己心灵原有的氤氲馨香。"]
print(ws.segment(sentence))