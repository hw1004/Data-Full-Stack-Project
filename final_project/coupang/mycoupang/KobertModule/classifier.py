# torch
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np

#kobert
from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel
from mycoupang.KobertModule.BERTClasses import BERTClassifier, BERTDataset

from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup

#GPU 사용
device = torch.device("cuda:0")

#BERT 모델, Vocabulary 불러오기
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)
vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

# Setting parameters
max_len = 64
batch_size = 64
warmup_ratio = 0.1
num_epochs = 5
max_grad_norm = 1
log_interval = 200
learning_rate =  5e-5

## 학습 모델 로드
PATH = '/home/lab04/final_project/coupang/mycoupang/KobertModule/model_state_dict.pt' # 경로에 맞게 수정필요
model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)
# model = torch.load(PATH + 'KoBERT_star.pt')  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
model.load_state_dict(torch.load(PATH, map_location='cpu'))  # state_dict를 불러 온 후, 모델에 저장
model.eval()

#토큰화
tok = tokenizer.tokenize

def new_softmax(a) : 
    c = np.max(a) # 최댓값
    exp_a = np.exp(a-c) # 각각의 원소에 최댓값을 뺀 값에 exp를 취한다. (이를 통해 overflow 방지)
    sum_exp_a = np.sum(exp_a)
    y = (exp_a / sum_exp_a) * 100
    return np.round(y, 3)


# 예측 모델 설정
def predict(predict_sentence):

    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, vocab, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)

    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length= valid_length
        label = label.long().to(device)

        out = model(token_ids, valid_length, segment_ids)

        test_eval=[]
        for i in out:
            logits=i
            logits = logits.detach().cpu().numpy()

            if np.argmax(logits) == 0:
                test_eval.append("★")
            elif np.argmax(logits) == 1:
                test_eval.append("★★")
            elif np.argmax(logits) == 2:
                test_eval.append("★★★")
        
        print(">> 입력하신 리뷰는 " + test_eval[0] + " 로 예측됩니다.")
    return test_eval[0]