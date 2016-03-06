import json
import colander
import itertools
import numpy as np
from json_deserializer import Properties
from json_deserializer import Functionalities


def generator(n,combinationf,combinationp):
    #for i in xrange(0, n):
#
#        chose=random.randint(1,len(combination))
#        print "scelta combinazione "+str(chose)
    pp=[]
    for combo in combinationp:
        pp.append(combo["prob"])
    pf=[]
    i=0
    for combo in combinationf:
        #print str(i)
        #print combo
        i=i+1
        pf.append(combo[-1]["prob"])
    extraction=list(np.random.choice(len(combinationf),n,pf))
    print extraction
    sequence=[]
    index=0
    for ex in extraction:
        #print combinationf[ex]
        single_seq=[]
        for f in combinationf[ex][:-1]:
            cert=list(np.random.choice(len(combinationp),1,pp))
            properties=[]
            for key in combinationp[cert[0]]["combo"]:
                singlep={"property":key["name"],"level":key["rank"]}
                properties.append(singlep)
            value={"function":f["function"],"cert":properties}
            single_seq.append(value)
        value={"id":index,"requestComposition":single_seq}
        sequence.append(value)
        index=index+1

    return sequence


#return a list of all possible combination of property and level
def get_property_card(property):
    with open(property) as pp:
        #print pp.read()
        schema = Properties()

        try:
            properties = schema.deserialize(json.loads(pp.read()))
        except colander.Invalid, e:
            errors = e.asdict()
            print "ERRORE"
            print errors
        #print deserialized
        allp=[];
        for p in properties:
            singleP=[]
            for level in p["levels"]:
                #print p['name']
                #print level
                value={'name':p['name'],'rank':level['rank'],'prob':level['p']}
                #print value
                singleP.append(dict(value))
            allp.append(singleP)

        combo_P=list(itertools.product(*allp))
        #p=1.0/len(combo_P)
        combo=[]
        for combos in combo_P:
            app=list(combos)
            p=1.0
            for prop in app:
              p=p*prop["prob"]
            value={'combo':app,'prob':p}
            combo.append(dict(value))
        return combo

def load_functionality(file):
    with open(file) as ff:
        #print pp.read()
        schema = Functionalities()

        try:
            functionalities = schema.deserialize(json.loads(ff.read()))
        except colander.Invalid, e:
            errors = e.asdict()
            print "ERRORE"
            print errors
        #print deserialized
        combo_f=[]
        for k in range(1,len(functionalities)+1):
            combo_app=list(itertools.combinations(functionalities,k))
            combo_f.extend(combo_app)
        #combo_f=list(itertools.combinations(functionalities,5))
        num=len(combo_f)
        p=1.0/num
        res=[]
        for c in combo_f:
            app=list(c)
            value={'prob':p}
            app.append(dict(value))

            res.append(app)
            #app.append()
        #p=1.0/len(combo_P)
        return res

if __name__ == '__main__':
    prop=get_property_card("data/property.json")
    i=1

    res=load_functionalityALL("data/function.json",prop)
    #ris=get_combination_FP(res,prop)
    #for r in ris:
    #    print i
    #    i=i+1
    #    print ris