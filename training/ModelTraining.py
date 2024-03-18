from happytransformer import HappyTextClassification, TCTrainArgs
happy_tc = HappyTextClassification(model_type="DISTILBERT",
                                   model_name="distilbert-base-uncased-finetuned-sst-2-english",
                                   num_labels=2)
args = TCTrainArgs(num_train_epochs=5)
before_loss = happy_tc.eval("ellipsis dataset.csv").loss
happy_tc.train("ellipsis dataset.csv", args=args)
after_loss = happy_tc.eval("ellipsis dataset.csv").loss
print("Before loss: ", before_loss)
print("After loss: ", after_loss)  
happy_tc.save("ellipsis/")