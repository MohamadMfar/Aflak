import torch
import pickle
from transformers import AutoConfig, AutoTokenizer, AutoModel, TFAutoModel

# v3.0
model_name_or_path = "parsbert/"
config = AutoConfig.from_pretrained(model_name_or_path)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

# model = TFAutoModel.from_pretrained(model_name_or_path)  For TF
model = AutoModel.from_pretrained(model_name_or_path, output_hidden_states=True,ignore_mismatched_sizes=True)

def word_embedding_getter(list_of_words):


    indexed_tokens = tokenizer.convert_tokens_to_ids(list_of_words)
    segments_ids =  [1]*len(list_of_words)
    # print(segments_ids)
# Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])
    model.eval()
    print(tokens_tensor)
    print(segments_tensors)
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2]

    token_embeddings = torch.stack(hidden_states, dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1,0,2)
    # print(token_embeddings.size())
    token_vecs_cat = []
    for token in token_embeddings:
        cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]))
        token_vecs_cat.append(cat_vec)

    return token_vecs_cat

import numpy as np
vocab =pickle.load(open('vocab_farsi','rb'))
vocab=list(vocab)
print('model loaded')
emb_bert = {}

print('doing stuff')
for word in vocab:
    print(word)
    emb_bert[word] =word_embedding_getter([word.replace('آ','ا')])
# embs= word_embedding_getter(vocab[0:400])
print('dumping stuff')

pickle.dump(emb_bert, open('emb_farsiـwith_replace','wb'))





# vocab =pickle.load(open('vocab_farsi','rb'))
# vocab=list(vocab)
# print('model loaded')
# import pickle
# import numpy as np
#
# emb_bert = pickle.load(open('emb_farsiـwith_replace','rb'))
#
# print('doing stuff')
# for word in emb_bert:
#     print(word)
#     emb_bert[word] =emb_bert[word][0].numpy()
# # embs= word_embedding_getter(vocab[0:400])




