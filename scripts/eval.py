import argparse
import json
from qakgc.logger import set_logger

def hits_at_k(preds, ans, k):
    """accepts list of predictions and answers"""

    preds_k = preds[:k]

    any_in = lambda a, b: bool(set(a).intersection(b))

    return any_in(preds_k, ans)

def reciprocal_rank(preds, ans):

    reciprocal_rank = []
    for answer in ans:
        try:
            r_rank = 1/(preds.index(answer)+1)
        except ValueError:
            r_rank = 0

        reciprocal_rank.append(r_rank)
    return max(reciprocal_rank)


def evaluate(dataset_file, prediction_file, map_file, k):

    answers = []
    with open(dataset_file) as data_file:
        for line in data_file:
            data = json.loads(line)
            answer = [data['entity']]
            answers.append(answer)

    
    if map_file:
        with open(map_file) as mf:
            ent_map = json.load(mf)
    
    predictions = []
    with open(prediction_file) as f:
        for line in f:
            data = json.loads(line)
            preds = data['entities']
            if map_file:
                preds = [ent_map[pred] for pred in preds if pred != '']
            predictions.append(preds)

    score = 0
    rr = 0
    for i in range(len(predictions)):
        score += hits_at_k(predictions[i], answers[i], k)
        rr += reciprocal_rank(predictions[i], answers[i])

    total = len(predictions)
    hitsk = 100.0 * score / total
    rr = rr / total
    logger.info({'Hits@{}'.format(k): hitsk})
    logger.info({"MRR": rr})
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('datasetfile')
    parser.add_argument('predfile')
    parser.add_argument('k', type=int)
    parser.add_argument('--map_file', type=str)
    parser.add_argument('--logfile', type=str, default='eval.log')

    # parse command line arguments
    args = parser.parse_args()

    # set up logger
    logger = set_logger(args.logfile)

    logger.info(25*"-" + " Evaluation " + 25*"-")
    
    logger.info('Arguments: %s' % str(args))

    evaluate(args.datasetfile, args.predfile, args.map_file, args.k)
