from happytransformer import HappyTextToText, TTTrainArgs
args = TTTrainArgs(num_train_epochs=5)
structures = ["ellipsis, juxtaposition", "fronting", "inversion", "embedding"]
#for structure in structures:
happy_tt = HappyTextToText("T5", "t5-base")
before_loss = happy_tt.eval("datasets/t2t_inversion_dataset.csv").loss
happy_tt.train("datasets/t2t_inversion_dataset.csv", args=args)
after_loss = happy_tt.eval("datasets/t2t_inversion_dataset.csv").loss
print("inversion before loss: ", before_loss)
print("inversion after loss: ", after_loss)  
happy_tt.save("ttt_inversion/")