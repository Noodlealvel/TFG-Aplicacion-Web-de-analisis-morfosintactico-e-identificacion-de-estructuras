from happytransformer import HappyTextClassification, TCTrainArgs
args = TCTrainArgs(num_train_epochs=5)
structures = ["ellipsis, juxtaposition", "fronting", "inversion", "embedding"]
for structure in structures:
    happy_tc = HappyTextClassification(model_type="DISTILBERT",
                                   model_name="distilbert-base-uncased-finetuned-sst-2-english",
                                   num_labels=2)
    before_loss = happy_tc.eval("datasets/" + structure + "_dataset.csv").loss
    happy_tc.train("datasets/" + structure + "_dataset.csv", args=args)
    after_loss = happy_tc.eval("datasets/" + structure + "_dataset.csv").loss
    print(structure + " before loss: ", before_loss)
    print(structure + " after loss: ", after_loss)  
    happy_tc.save(structure + "/")