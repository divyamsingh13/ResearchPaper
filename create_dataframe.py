import pandas
import numpy
import six.moves.cPickle as pickle
import textract

text=textract.process("./pdfs/neural/A Hopfield Neural Network Based Building Agent for Detection and Correction of Programming Errors.pdf")
text=str(text)
keyword=text[text.find("Keywords:")+len("Keywords:"):text.find("Introduction")].split(',')
print(keyword)

f = open('train.pkl', 'wb')
pkl.dump((train_x, train_y), f, -1)
f.close()


f = open('train.pkl', 'rb')
reviews = pickle.load(f)
f.close()
