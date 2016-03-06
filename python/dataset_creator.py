from __future__ import print_function
from dataset import generator,get_property_card,load_functionality
from costFunction import CostCalculator
import random
import io, json

home_profile="../dataset/"

if __name__ == '__main__':
    alg=CostCalculator()
    combination=get_property_card(home_profile+"data/property.json")
    res=load_functionality(home_profile+"data/function.json")
    #0,0 0,1 0,2 1,0 1,1 1,2 2,0 2,1 2,2
    #sws=alg.input_pCostW(combination);
    costa=alg.property_based_fca(combination,[1,2,3])
    costb=alg.property_based_fcb(combination,[0,1,2])
    #costb=alg.property_based_fcb(combination,[0,3,4,3,5,6,4,6,7])
    costf=alg.function_cost_assignment([{"function":"f1"},{"function":"f2"},{"function":"f3"},{"function":"f4"},{"function":"f5"}])
    costfc=alg.function_cost_assignment_cert([{"function":"f1"},{"function":"f2"},{"function":"f3"},{"function":"f4"},{"function":"f5"}])
    deployed={"f1":None,"f2":None,"f3":None,"f4":None,"f5":None}


    #alg.choseDeployment(deployed,{'id': 0, 'requestComposition': [{'function': 'f2', 'cert': [{'property': 'p1', 'level': 0}, {'property': 'p2', 'level': 1}]}, {'function': 'f4', 'cert': [{'property': 'p1', 'level': 1}, {'property': 'p2', 'level': 0}]}]})
    #alg.choseDeployment(deployed,{'id': 0, 'requestComposition': [{'function': 'f2', 'cert': [{'property': 'p1', 'level': 0}, {'property': 'p2', 'level': 1}]}, {'function': 'f4', 'cert': [{'property': 'p1', 'level': 1}, {'property': 'p2', 'level': 0}]}]})

    sequence=generator(1000 ,res,combination)

    for i in xrange(0,10):
        s=list(sequence)
        random.shuffle(s)
        with io.open(home_profile+'dataset-'+str(i)+'.json', 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(s, ensure_ascii=False)))


    with io.open(home_profile+'dataset.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(sequence, ensure_ascii=False)))

    with io.open(home_profile+'deployment.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(deployed, ensure_ascii=False)))

    with io.open(home_profile+'costf.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(costf, ensure_ascii=False)))

    with io.open(home_profile+'costf_cert.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(costfc, ensure_ascii=False)))

    with io.open(home_profile+'costa.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(costa, ensure_ascii=False)))

    with io.open(home_profile+'costb.json', 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(costa, ensure_ascii=False)))