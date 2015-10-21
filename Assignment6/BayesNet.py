#!/usr/bin/env python
import argparse
import re

class ParentNode:
    def __init__(self, pTrue, name):
        # low = True
        self.pTrue = pTrue
        self.name = name
        self.cancerNode = None
    
    def probability(self, isTrue):
        prob = self.pTrue if isTrue else 1.0 - self.pTrue
        return prob
    
    def conditional(self, selfTrue, otherNode, isTrue):
        # P(self = selfTrue|otherNode = isTrue)
        prob = 0.0
        if (otherNode == self):
            prob = 1.0 if selfTrue else 0.0
        elif (isinstance(otherNode, ParentNode)):
            prob = self.probability(selfTrue)
        elif (otherNode == self.cancerNode):
            prob = otherNode.conditional(isTrue, self, selfTrue) * self.probability(selfTrue) / otherNode.probability(isTrue)
        else:
            # child node
            c = self.cancerNode.conditional(True, self, selfTrue)
            prob = otherNode.conditional(isTrue, self.cancerNode, True) * c + otherNode.conditional(isTrue, self.cancerNode, False) * (1 - c)
            prob *= self.probability(selfTrue) / otherNode.probability(isTrue)
        return prob
    
    def doubleConditional(self, selfTrue, node1, node2, isTrue1, isTrue2):
        # P(self = selfTrue|node1 = isTrue1, node2 = isTrue2)
        prob = 0.0
        if (node1 == self or node2 == self):
            prob = 1.0 if selfTrue else 0.0
        elif (node1 == self.cancerNode and isinstance(node2, ParentNode)):
            prob = self.cancerNode.doubleConditional(isTrue1, self, node2, selfTrue, isTrue2) * self.probability(selfTrue)
            prob /= self.cancerNode.conditional(isTrue1, node2, isTrue2)
        elif (isinstance(node1, ParentNode) and node2 == self.cancerNode):
            prob = self.cancerNode.doubleConditional(isTrue2, self, node1, selfTrue, isTrue1) * self.probability(selfTrue)
            prob /= self.cancerNode.conditional(isTrue2, node1, isTrue1)
        elif (isinstance(node1, ChildNode) and isinstance(node2, ParentNode)):
            prob = self.conditional(selfTrue, node1, isTrue1)
        elif (isinstance(node1, ParentNode) and isinstance(node2, ChildNode)):
            prob = self.conditional(selfTrue, node2, isTrue2)
        elif (isinstance(node1, ChildNode) and node2 == self.cancerNode):
            prob = node2.conditional(isTrue2, self, selfTrue) * node1.doubleConditional(isTrue1, node2, self, isTrue2, selfTrue)
            prob *= self.probability(selfTrue) / (node1.probability(isTrue1) * node2.conditional(isTrue2, node1, isTrue1))
        elif (isinstance(node2, ChildNode) and node1 == self.cancerNode):
            prob = node1.conditional(isTrue1, self, selfTrue) * node2.doubleConditional(isTrue2, node1, self, isTrue1, selfTrue)
            prob *= self.probability(selfTrue) / (node2.probability(isTrue2) * node1.conditional(isTrue1, node2, isTrue2))
        else:
            prob = node1.conditional(isTrue1, self, selfTrue) * node2.doubleConditional(isTrue2, node1, self, isTrue1, selfTrue)
            prob *= self.probability(selfTrue) / (node1.probability(isTrue1) * node2.conditional(isTrue2, node1, isTrue1))
        return prob
    
class ChildNode:
    def __init__(self, pTrueCTrue, pTrueCFalse, cancerNode, name):
        self.pTrueCTrue = pTrueCTrue
        self.pTrueCFalse = pTrueCFalse
        self.cancerNode = cancerNode
        self.name = name
    
    def probability(self, isTrue):
        pTrue = self.pTrueCTrue * self.cancerNode.probability(True) + self.pTrueCFalse * self.cancerNode.probability(False)
        prob = pTrue if isTrue else 1.0 - pTrue
        return prob
    
    def conditional(self, selfTrue, otherNode, isTrue):
        # P(self = selfTrue|otherNode = isTrue)
        prob = 0.0
        if (otherNode == self):
            prob = 1.0 if selfTrue else 0.0
        elif (otherNode == self.cancerNode):
            p = self.pTrueCTrue if isTrue else self.pTrueCFalse
            prob = p if selfTrue else 1.0 - p
        else:
            c = self.cancerNode.conditional(True, otherNode, isTrue)
            prob = self.conditional(selfTrue, self.cancerNode, True) * c + self.conditional(selfTrue, self.cancerNode, False) * (1 - c)
        return prob
    
    def doubleConditional(self, selfTrue, node1, node2, isTrue1, isTrue2):
        # P(self = selfTrue|node1 = isTrue1, node2 = isTrue2)
        prob = 0.0
        if (node1 == self or node2 == self):
            prob = 1.0 if selfTrue else 0.0
        elif (node1 == self.cancerNode and isinstance(node2, ParentNode)):
            prob = self.conditional(selfTrue, self.cancerNode, isTrue1)
        elif (node2 == self.cancerNode and isinstance(node1, ParentNode)):
            prob = self.conditional(selfTrue, self.cancerNode, isTrue2)
        elif (isinstance(node1, ParentNode) and isinstance(node2, ParentNode)):
            prob = node1.conditional(isTrue1, self, selfTrue) * node2.conditional(isTrue2, self, selfTrue)
            prob *= self.probability(selfTrue) / (node1.probability(isTrue1) * node2.probability(isTrue2))
        else:
            # one child, one parent
            c = self.cancerNode.doubleConditional(True, node1, node2, isTrue1, isTrue2)
            prob = self.conditional(selfTrue, self.cancerNode, True) * c + self.conditional(selfTrue, self.cancerNode, False) * (1 - c)
        return prob

class CancerNode:
    def __init__(self, pollutionNode, smokerNode):
        self.pollutionNode = pollutionNode
        self.smokerNode = smokerNode
        self.probabilityTable = [(False, True, 0.05), (False, False, 0.02), (True, True, 0.03), (True, False, 0.001)]
        self.name = "Cancer"
    
    def probability(self, isTrue):
        pTrue = 0.0
        for p, s, val in self.probabilityTable:
            pTrue += val * self.pollutionNode.probability(p) * self.smokerNode.probability(s)
        prob = pTrue if isTrue else 1.0 - pTrue
        return prob
    
    def conditional(self, selfTrue, otherNode, isTrue):
        # P(self = selfTrue|otherNode = isTrue)
        prob = 0.0
        if (otherNode == self):
            prob = 1.0 if selfTrue else 0.0
        elif (otherNode == self.pollutionNode):
            for p, s, val in self.probabilityTable:
                if (p == isTrue):
                    prob += val * self.smokerNode.probability(s)
            prob = prob if selfTrue else 1.0 - prob
        elif (otherNode == self.smokerNode):
            for p, s, val in self.probabilityTable:
                if (s == isTrue):
                    prob += val * self.pollutionNode.probability(p)
            prob = prob if selfTrue else 1.0 - prob
        else:
            prob = otherNode.conditional(isTrue, self, selfTrue) * self.probability(selfTrue) / otherNode.probability(isTrue)
        return prob
    
    def doubleConditional(self, selfTrue, node1, node2, isTrue1, isTrue2):
        # P(self = selfTrue|node1 = isTrue1, node2 = isTrue2)
        prob = 0.0
        if (node1 == self or node2 == self):
            prob = 1.0 if selfTrue else 0.0
        elif (node1 == self.pollutionNode and node2 == self.smokerNode):
            for p, s, val in self.probabilityTable:
                if (p == isTrue1 and s == isTrue2):
                    prob += val
            prob = prob if selfTrue else 1.0 - prob
        elif (node2 == self.pollutionNode and node1 == self.smokerNode):
            for p, s, val in self.probabilityTable:
                if (p == isTrue2 and s == isTrue1):
                    prob += val
            prob = prob if selfTrue else 1.0 - prob
        else:
            prob = node1.conditional(isTrue1, self, selfTrue) * node2.doubleConditional(isTrue2, self, node1, selfTrue, isTrue1)
            prob *= self.probability(selfTrue) / (node1.probability(isTrue1) * node2.conditional(isTrue2, node1, isTrue1))
        return prob
    
def makeTable(node1, node2, node3, isTrue1, isTrue2, isTrue3):
    for i in [True, False]:
        for j in [True, False]:
            for k in [True, False]:
                if ((i == isTrue1 or isTrue1 == None) and (j == isTrue2 or isTrue2 == None) and (k == isTrue3 or isTrue3 == None)):
                    p = node1.probability(i) * node2.conditional(j, node1, i) * node3.doubleConditional(k, node1, node2, i, j)
                    print "P(", node1.name,"=",i,",",node2.name,"=",j,",",node3.name,"=",k,") =",p

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-g", help="Conditional probability",
                           type=str, default=None, required=False)
    argparser.add_argument("-j", help="Joint probability",
                           type=str, default=None, required=False)
    argparser.add_argument("-m", help="Marginal probability",
                           type=str, default=None, required=False)
    argparser.add_argument("-pP", help="Set probability for Pollution=Low",
                           type=float, default=0.9, required=False)
    argparser.add_argument("-pS", help="Set probability for Smoker=True",
                           type=float, default=0.3, required=False)
    args = argparser.parse_args()
    
    smokerNode = ParentNode(args.pS, "Smoker")
    pollutionNode = ParentNode(args.pP, "Pollution")
    cancerNode = CancerNode(pollutionNode, smokerNode)
    xrayNode = ChildNode(0.9, 0.2, cancerNode, "XRay")
    dNode = ChildNode(0.65, 0.3, cancerNode, "Dyspnoea")
    
    smokerNode.cancerNode = cancerNode
    pollutionNode.cancerNode = cancerNode
    
    nodes = {'S' : smokerNode, 'P' : pollutionNode, 'C' : cancerNode, 'X': xrayNode, 'D' : dNode}
    if (args.g != None):
        a = args.g.split(":")[0]
        b = args.g.split(":")[1]
        aNode = None
        isTrue = True
        if (len(a) == 1):
            aNode = nodes.get(a.capitalize())
        else:
            aNode = nodes.get(a[1].capitalize())
            isTrue = False
        if len(b) == 1:
            bNode = nodes.get(b.capitalize())
            print "Bel(", aNode.name, "=", isTrue, "|", bNode.name, "= True ) =", aNode.conditional(isTrue, bNode, True)
        else:
            bNode1 = nodes.get(b[0].capitalize())
            bNode2 = nodes.get(b[1].capitalize())
            p = aNode.doubleConditional(isTrue, bNode1, bNode2, True, True)
            print "Bel(", aNode.name, "=", isTrue, "|", bNode1.name, "= True,", bNode2.name, "= True ) =", p
    elif (args.j != None):
        match = re.match(r'(~?)(\w{1})(~?)(\w{1})(~?)(\w{1})', args.j)
        if match:
            b = []
            for i in [1, 3, 5]:
                if (match.group(i+1).islower()):
                    bi = True if match.group(i) == "" else False
                else:
                    bi = None
                b.append(bi)
                b.append(nodes.get(match.group(i+1).capitalize()))
            makeTable(b[1], b[3], b[5], b[0], b[2], b[4])
        else:
            print "No match"
        
    elif (args.m != None):
        node = nodes.get(args.m)
        print "Bel(", node.name, "= True ) =", node.probability(True)
