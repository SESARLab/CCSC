import random
import copy


class CostCalculator(object):
#           0       1           2       3           4           5       6           7           8           9
    pw=[[0.,4,0],[0.33,110,0],[0.66,150,0],[1,150,0],[0.35,7,0],[0.4,6,0],[0.45,10,0],[0.5,7,0.],[0.5,10,0.],[0.5,10,0.1]]
    pw_cert=[[0.,20,3,1.4,1.8],[0.33,40,4,1.05,1.3],[0.66,33,2,1.1,1.5],[1,150,0],[0.35,7,0],[0.4,6,0],[0.45,10,0],[0.5,7,0.],[0.5,10,0.],[0.5,10,0.1]]

#pw         elem 0  impulso base, elem 1 frequenza elem 2 minimo
#pw_cert    elem 0  impulso base, elem 1 frequenza, elem 2 frequenza incremento elem 3 lowerbound elem 4 upperbound
    MAX=1
    MIN=0
#w1 = 0.6; w2 = 0.3; w3 = 0.1
#w1 = 0.1; w2 = 0.3; w3 = 0.6
#w1 = 0.33; w2 = 0.33; w3 = 0.33
    wdc=0.33
    wcc=0.33
    wic=0.33
    N=1000
    randshift=0

    #random value between randmax and randmin divided per 10 is random signal amplification
    randmin=10
    randmax=10

    lower_amp=1.4
    upper_amp=1.8

# prima prova 5f 1p 3l -> 0,333 0,66 1  -----




    def getCostDC(self):
        return self.costf

    def setCostDC(self,costDC):
        self.costf=costDC

    def setCost_Cert(self,cost_cert):
        self.costf_cert=cost_cert



    def input_pCostW(self,c_properties):
        ws=[]
        for combo in c_properties:
            print combo
            ws.append(int(raw_input('Weight:')))
            print "\n\n\n\n -------------------------------------------------\n"
        return ws

    def property_based_fcb(self,c_properties,weigths):
        print "Assign a weight from 0 to 9 to each property combination"
        fcostp=[]
        w=0
        for combo in c_properties:
            print combo
            pwUser=weigths[w]
            amp=random.uniform(self.pw_cert[pwUser][3],self.pw_cert[pwUser][4])
            amp_count=1;
            freq=int(self.N/self.pw[pwUser][1])
            fcost=[]
            fcost.append(0)
            fcost.append(self.MAX*self.pw[pwUser][0])
            impulse=self.MAX*self.pw[pwUser][0]
            for i in xrange(2,self.N):
                if i%freq==0:
                    if(amp_count%self.pw_cert[pwUser][2]==0):
                        impulse=impulse*amp
                        if(impulse>1):
                            impulse=1
                    fcost.append(impulse)
                    amp_count+=1
                else:
                  fcost.append(0)

            value={"combo":combo["combo"],"fcost":fcost}
            fcostp.append(value)
            self.costpb=fcostp
            w=w+1
        return fcostp


    def property_based_fca(self,c_properties,weigths):
        print "Assign a weight from 0 to 9 to each property combination"
        fcostp=[]
        w=0
        for combo in c_properties:
            print combo
            pwUser=weigths[w]
            freq=int(self.N/self.pw[pwUser][1])
            fcost=[]
            fcost.append(0)
            fcost.append(self.MAX*self.pw[pwUser][0])
            for i in xrange(2,self.N):
                if i%freq==0:
                    fcost.append(self.MAX*self.pw[pwUser][0])
                else:
                    fcost.append(self.MIN+self.pw[pwUser][2])

            value={"combo":combo["combo"],"fcost":fcost}
            fcostp.append(value)
            self.costpa=fcostp
            w=w+1
        return fcostp

    def equalCombo(self,comboa,combob):
        for pr in comboa:
            found=False
            for pd in combob:
                if pr["name"]==pd["name"] and pr["rank"]==pd["rank"]:
                    found=True
                    break
            if not found:
                return False
        return True


    def sumCostAlphaCostBeta(self):
        print self.costpa
        costp=copy.deepcopy(self.costpa)
        for fa in costp:
            for fb in self.costpb:
                if self.equalCombo(fb["combo"],fa["combo"]):
                    for i in xrange(0,len(fa["fcost"])):
                        if i == 1:
                            print fa["fcost"][i]
                            print fb["fcost"][i]
                        fa["fcost"][i]=fa["fcost"][i]+fb["fcost"][i]
                        if i == 1:
                            print fa["fcost"][i]
                        #print "-----"
        #print self.costpb
        #print self.costpa
        #print costp
        #print self.costpa
        #print costp
        return costp

    def function_cost_assignment(self,function):
        costp= self.costpa;

        #costp=[x + y for x, y in zip(self.costpa, self.costpb)]
        #costp=self.costpa+self.costpb
        print "assignment of cost function to tasks"
        allfcost=[]
        for f in function:
            fcost=[]
            for c in costp:
                nc = list(c["fcost"])
                amp=random.randint(self.randmin, self.randmax)
                amp=amp/10.0
                print "VARIATION "+str(amp)
                signal=nc[1]
                i=0
                for value in nc:
                    app=value
                    nc[i]=value*amp
                    if app==signal:
                        shift=random.randint(-1*self.randshift,self.randshift)

                        print "PHASE "+str(shift)
                        #if(i+shift<len(nc) and (i+shift>1)) and (i!=1):
                        #    nc[i], nc[i+shift] = nc[i+shift], nc[i]
                    i=i+1
                value={"cert":c["combo"],"fcost":nc}
                fcost.append(value);
            value={"function":f["function"],"deployment":fcost}
            allfcost.append(value)
        self.costf=allfcost
        return allfcost


    def function_cost_assignment_cert(self,function):
        costp= self.costpb;

        #costp=[x + y for x, y in zip(self.costpa, self.costpb)]
        #costp=self.costpa+self.costpb
        print "assignment of cost function to tasks"
        allfcost=[]
        for f in function:
            fcost=[]
            for c in costp:
                nc = list(c["fcost"])
                amp=random.randint(self.randmin, self.randmax)
                amp=amp/10.0
                #print "VARIATION "+str(amp)
                signal=nc[1]
                i=0
                for value in nc:
                    app=value
                    nc[i]=value*amp
                    if app==signal:
                        shift=random.randint(-1*self.randshift,self.randshift)
                        #print "PHASE "+str(shift)
                        #if(i+shift<len(nc) and (i+shift>1)) and (i!=1):
                        #    nc[i], nc[i+shift] = nc[i+shift], nc[i]
                    i=i+1
                value={"cert":c["combo"],"fcost":nc}
                fcost.append(value);
            value={"function":f["function"],"deployment":fcost}
            allfcost.append(value)
        self.costf_cert=allfcost
        return allfcost


    def comp_checker(self,d,r):
        for fr in r:
            found=False;
            for p in d:
                if fr["property"]==p["property"] and fr["level"]<=p["level"]:
                    found=True
                    break
            if found==False:
                return False
        return True






    def get_compatible(self,deployed,todeploy):
        comp=[]
        for d in deployed:
                res=self.comp_checker(d["cert"],todeploy)
                if res:
                    comp.append(d)
        return comp

    def getTask(self,argument):
        switcher = {'f1': 0,
            'f2': 1,
            'f3': 2,
            'f4': 3,
            'f5': 4,
            }
        return switcher.get(argument, None)

    def getDCCost(self,fun,request):

        for f in self.costf:
            if fun==f["function"]:
                deployment=f["deployment"]
                for d in deployment:
                    confd=d["cert"]
                    confr=request["cert"]
                    found=self.equal(confd,confr)
                    if found:
                        #print "FUNZIONE DI COSTO"
                        #print d
                        #print request
                        #print d["fcost"][request["k"]+1]
                        try:
                            return d["fcost"][request["k"]+1]
                        except Exception:
                            print "errore"


    #differenza per k=1
    def getICCost(self,c,r):

        diff=[]
        for pr in r:
            for pc in c:
                if pc["property"]==pr["property"]:

                    diff.append((pc["level"]-pr["level"])*(1./3.))
                    break
        res=sum(diff) / float(len(diff))
        return res


    def getCertCost(self,fun,request):

        for f in self.costf_cert:
            if fun==f["function"]:
                deployment=f["deployment"]
                for d in deployment:
                    confd=d["cert"]
                    confr=request["cert"]
                    found=self.equal(confd,confr)
                    if found:
                        #print "FUNZIONE DI COSTO"
                        #print d
                        #print request
                        #print d["fcost"][request["k"]+1]
                        try:
                            return d["fcost"][request["k"]+1]
                        except Exception:
                            print "errore"


    def equal(self,certd,certr):

        for pr in certr:
            found=False
            for pd in certd:
                if pr["property"]==pd["name"] and pr["level"]==pd["rank"]:
                    found=True
                    break
            if not found:
                return False
        return True


    def equal2(self,certd,certr):

        for pr in certr:
            found=False
            for pd in certd:
                if pr["property"]==pd["property"] and pr["level"]==pd["level"]:
                    found=True
                    break
            if not found:
                return False
        return True




            #if equal(f,)

    def choseDeployment(self,deployed, todeploy):
        #print deployed
        #print "REQUEST"
        request=todeploy["requestComposition"]
        costo_totale=0
        result={"cost":costo_totale,"newDeployment":0,"costdc":0,"costic":0,"costc":0}
        newDeployment=False
        for f in request:
            #print f["function"]
            #print f["cert"]
           #index=self.getTask(f["function"]
            cost=0

            if deployed[f["function"]] is None:
                deployed[f["function"]]=[]
                value={"cert":f["cert"],"k":1}
                tocost={"cert":f["cert"],"k":0}
                deployed[f["function"]].append(value)
                costDC=self.getDCCost(f["function"],tocost)
                cost_c=self.getCertCost(f["function"],tocost)
                cost=self.wdc*costDC+self.wcc*cost_c
                result["newDeployment"]=result["newDeployment"]+1
                min={"cost":cost,"i":0,"costdc":costDC,"costic":0,"costc":cost_c}

            else:
                candidate=self.get_compatible(deployed[f["function"]],f["cert"])
                #candidate contains itself?
                found=False
                for c in candidate:
                    if self.equal2(c["cert"],f["cert"]):
                        found=True
                        break

                #prova todo
                #if found == False :
                    #print "POSSIBLE NEW D"
                candidate.append({"cert":f["cert"],"k":0})
                #if not candidate:
                #    value={"cert":f["cert"],"k":1}
                #    tocost={"cert":f["cert"],"k":0}
                #    deployed[f["function"]].append(value)
                #    cost=self.getDCCost(f["function"],tocost)
                #    costIC=
                #else:
                i=0
                for c in candidate:
                    costDC=self.getDCCost(f["function"],c)
                    #print costDC
                    costIC=self.getICCost(c["cert"],f["cert"])
                    cost_c=self.getCertCost(f["function"],c)
                    try:
                        cost=self.wdc*costDC+self.wic*costIC+self.wcc*cost_c
                    except Exception:
                        print "errore"
                    if i==0:
                        min={"cost":cost,"i":i,"costdc":costDC,"costic":costIC,"costc":cost_c}
                    else:
                        if cost < min["cost"] :
                            min["cost"]=cost
                            min["costdc"]=costDC
                            min["costic"]=costIC
                            min["costc"]=cost_c
                            min["i"]=i
                    i=i+1;
                cost=min["cost"]
                if( candidate[min["i"]]["k"] == 0 ):
                    value={"cert":f["cert"],"k":1}
                    deployed[f["function"]].append(value)
                    result["newDeployment"]=result["newDeployment"]+1
                else:
                    candidate[min["i"]]["k"]=candidate[min["i"]]["k"]+1
            costo_totale=costo_totale+cost
            result["cost"]=costo_totale
            result["costc"]=result["costc"]+min["costc"]
            result["costdc"]=result["costdc"]+min["costdc"]
            result["costic"]=result["costic"]+min["costic"]
        #print "------------------------------------------------\n\n"
        #print deployed
            #candidate=get_compatible(deployed,todeploy)
        #if  costo_totale==0:
        #    print "EVVIVA"
        #else:
        #    print "-"
        #return costo_totale
        #print result
        return result

if __name__ == '__main__':
    app=CostCalculator()
    deployed={"f1":None,"f2":None,"f3":None,"f4":None,"f5":None}
    app.choseDeployment(deployed,{'id': 0, 'requestComposition': [{'function': 'f2', 'cert': [{'property': 'p1', 'level': 0}, {'property': 'p2', 'level': 1}]}, {'function': 'f4', 'cert': [{'property': 'p1', 'level': 1}, {'property': 'p2', 'level': 0}]}]})
    print deployed
    app.choseDeployment(deployed,{'id': 0, 'requestComposition': [{'function': 'f2', 'cert': [{'property': 'p1', 'level': 0}, {'property': 'p2', 'level': 1}]}, {'function': 'f4', 'cert': [{'property': 'p1', 'level': 1}, {'property': 'p2', 'level': 0}]}]})
    print deployed
