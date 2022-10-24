from ckip_transformers.nlp import CkipWordSegmenter
# Initialize drivers with custom checkpoints
ws_driver  = CkipWordSegmenter(model_name='ckiplab/bert-base-chinese-ws')
# Input text
text = [
   "可以用初中学过的这首诗来表达:“我如果爱你，绝不像攀援的凌霄花，借你的高枝炫耀自己；我必须是你近旁的一株木棉，作为树的形象和你站在一起。我们分担寒潮、风雷、霹雳；我们共享雾霭、流岚、虹霓。不仅爱你伟岸的身躯，也爱你坚持的位置，足下的土地。”"
]

# Run pipeline
ws  = ws_driver(text)
for sentence, sentence_ws in zip(text, ws):
   print(sentence)
   print(sentence_ws)