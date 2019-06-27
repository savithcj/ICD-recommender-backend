from api import serializers
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Length
from recommendations.models import Rule, Code, TreeCode, CodeBlockUsage, DaggerAsterisk
from itertools import combinations
from django.http import HttpResponse
from django.forms.models import model_to_dict
import json
from django.db.models import Q

# TODO: implement access permissions?


@permission_classes((permissions.AllowAny,))
class ModifyRule(APIView):

    def put(self, request, format=None, **kwargs):
        body = request.body.decode('utf-8')
        body_data = json.loads(body)
        LHSCodes = ''
        RHSCodes = ''
        ageStart = None
        ageEnd = None
        gender = ''

        if len(body_data['LHSCodes']) < 1 or len(body_data['RHSCodes']) != 1:
            print("Wrong number of items in fields, rule not created.")
            return HttpResponse(400)

        LHSCodesList = list(body_data['LHSCodes'])
        LHSCodesList.sort()
        for counter, code in enumerate(LHSCodesList):
            LHSCodes = LHSCodes + str(code)
            if counter < len(body_data['LHSCodes']) - 1:
                LHSCodes = LHSCodes + ','

        RHSCodesList = list(body_data['RHSCodes'])
        RHSCodesList.sort()
        for counter, code in enumerate(RHSCodesList):
            RHSCodes = RHSCodes + str(code)
            if counter < len(body_data['RHSCodes']) - 1:
                RHSCodes = RHSCodes + ','

        if 'ageStart' in body_data:
            ageStart = int(body_data['ageStart'])
        else:
            ageStart = 0

        if 'ageEnd' in body_data:
            ageEnd = int(body_data['ageEnd'])
        else:
            ageEnd = 0

        # FIXME: gender not implemented in Rule
        if 'gender' in body_data:
            gender = body_data['gender']
        else:
            pass

        if 'id' in body_data and body_data['id'] != '':
            # Modifying a rule
            pass
        else:
            newRule = Rule.objects.create(
                lhs=LHSCodes, rhs=RHSCodes, min_age=ageStart, max_age=ageEnd)
            newRule.save()

        return HttpResponse(201)


@permission_classes((permissions.AllowAny,))
class FlagRuleForReview(generics.ListAPIView):
    def put(self, request, ruleId, format=None, **kwargs):
        print("ruleId=" + ruleId)

        try:
            ruleObj = Rule.objects.get(id=ruleId)
            ruleObj.num_flags += 1
            if ruleObj.active is True and ruleObj.review_status == 0:
                ruleObj.review_status = 1  # set to user flagged for admin review status
                # ruleObj.active = False  # disables rule from showing
            ruleObj.save()
            return HttpResponse(200)

        except Exception as e:
            print(e)
            return HttpResponse(400)


@permission_classes((permissions.AllowAny,))
class RuleSearch(generics.ListAPIView):

    def post(self, request, format=None, **kwargs):
        body = request.body.decode('utf-8')
        body_data = json.loads(body)
        LHSCodesList = list(body_data["LHSCodes"])
        RHSCodesList = list(body_data["RHSCodes"])

        if len(LHSCodesList) < 1 and len(RHSCodesList) < 1:
            print("Nothing entered in search.")
            return HttpResponse(400)

        rules = Rule.objects.all()

        for code in LHSCodesList:
            rules = rules.filter(lhs__icontains=code)

        for code in RHSCodesList:
            rules = rules.filter(rhs__icontains=code)

        serializer = serializers.RulesSerializer(rules, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListAllRules(generics.ListAPIView):
    """
    Lists all rules
    """
    queryset = Rule.objects.all()
    serializer_class = serializers.RulesSerializer


@permission_classes((permissions.AllowAny,))
class ListCodeBlockUsage(APIView):
    def get(self, request, format=None, **kwargs):
        blocks = CodeBlockUsage.objects.all()
        for block in blocks:
            blockObject = TreeCode.objects.get(code=block.block)
            block.description = blockObject.description
            block.parent = blockObject.parent
            parentObject = TreeCode.objects.get(code=block.parent)
            block.parent_description = parentObject.description
        serializer = serializers.CodeBlockUsageSerializer(blocks, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class SingleCodeDescription(APIView):
    def get(self, request, inCode, format=None, **kwargs):
        try:
            codeObject = Code.objects.get(code=inCode)
        except ObjectDoesNotExist:
            return Response({None})
        serializer = serializers.CodeSerializer(codeObject, many=False)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListChildrenOfCode(APIView):
    def get_object(self, inCode):
        try:
            childrenCodes = Code.objects.get(code=inCode).children
            childrenCodes = childrenCodes.split(",")
            children = Code.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get(self, request, inCode, format=None, **kwargs):
        children = self.get_object(inCode)
        serializer = serializers.CodeSerializer(children, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListRequestedRules(APIView):
    def get_object(self, inCodes, request):
        try:
            # Sort input codes
            inputCodes = inCodes
            inputRules = inputCodes.split(",")
            inputRules.sort()

            # Build combinations of codes
            # max combination in the LHS of 5 codes
            lhs = []
            for i in range(min(len(inputRules), 5)):
                lhs += list(combinations(inputRules, i+1))

            # Concatening items in combinations together
            new_lhs = []
            for entry in lhs:
                empty = ''
                for i in range(len(entry)):
                    empty += entry[i] + ","
                new_lhs.append(empty[:-1])

            # special params
            kwargs = dict()
            kwargs["min_age"] = None
            kwargs["max_age"] = None
            kwargs["gender"] = None

            # TODO: Implement gender

            ageRange = [65, 45, 20, 0]
            age_param = request.GET.get('age', None)
            if age_param is not None and age_param.isdigit():
                age = int(age_param)
                print("In Age:", age)
                for minAge in ageRange:
                    if age >= minAge:
                        kwargs["min_age"] = minAge
                        print("Min Age:", minAge)
                        break
                pass

            # get rules
            # sqllite has max query param size of 999
            # werid stuff below to get around max param size. have to get rule ids and then query the rules.
            # direct query will cause overflow of param size
            maxSqlParams = 900
            ruleIds = []
            for i in range(0, len(new_lhs), maxSqlParams):
                temp_lhs = new_lhs[i:i+maxSqlParams]
                tempRules = Rule.objects.filter(
                    lhs__in=temp_lhs, **{k: v for k, v in kwargs.items() if v is not None}, active=True)
                for rule in tempRules:
                    ruleIds.append(rule.id)

            # construct a new queryset of rules because the old queryset would cause max param size error
            # exclude rules with code in RHS that already exist in the LHS
            rules = Rule.objects.filter(id__in=ruleIds).exclude(rhs__iregex=r'(' + '|'.join(new_lhs) + ')')
            for rule in rules:
                code = Code.objects.get(code=rule.rhs)
                rule.description = code.description
            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, inCodes, format=None, **kwargs):
        rules = self.get_object(inCodes, request)
        serializer = serializers.ExtendedRulesSerializer(rules, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class DaggerAsteriskAPI(APIView):
    def get_object(self, inCodes, request):
        try:
            # Getting input codes
            inputCodes = inCodes
            inputCodes = inputCodes.split(",")

            # Getting combinations with the codes in either dagger or asterisk
            rules = DaggerAsterisk.objects.filter(Q(dagger__in=inputCodes) | Q(asterisk__in=inputCodes))
            # Removing combinations with code in both the dagger and asterisk
            rules = rules.exclude(asterisk__in=inputCodes, dagger__in=inputCodes)
            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, inCodes, format=None, **kwargs):
        rules = self.get_object(inCodes, request)
        serializer = serializers.daggerAsteriskSerializer(rules, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListFlaggedRules(APIView):
    def get_objects(self):
        try:
            rules = Rule.objects.filter(review_status=1)

            # append description
            for rule in rules:
                rule.description = "Suggested: "+str(rule.num_suggested) + ", " + \
                    "Accepted: "+str(rule.num_accepted)+", "+"Rejected: "+str(rule.num_rejected)

            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, format=None, **kwargs):
        rules = self.get_objects()
        serializer = serializers.ExtendedRulesSerializer(rules, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class UpdateFlaggedRule(APIView):

    def put(self, request, ruleIdAndDecision, format=None, **kwargs):
        ruleId, decision = ruleIdAndDecision.split(",")
        try:
            rule = Rule.objects.get(id=ruleId)
            print(rule.review_status)
            if(rule.review_status == 0):
                print("Not a flagged rule")
                return HttpResponse(status=400)
            if(rule.review_status == 2 or rule.review_status == 3):
                print("Rule already reviewed")
                return HttpResponse(status=400)
            if(decision == "ACCEPT"):
                rule.review_status = 2
                rule.active = True
            elif(decision == "REJECT"):
                rule.review_status = 3
                rule.active = False
            else:
                print("Error evaluating decision => "+decision)
                return HttpResponse(status=400)

            rule.save()
            print("Succesfully updated rule")
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)


@permission_classes((permissions.AllowAny,))
class Family(APIView):
    def get_children(self, inCode):
        try:
            childrenCodes = TreeCode.objects.get(code=inCode).children
            childrenCodes = childrenCodes.split(",")
            children = TreeCode.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get_siblings(self, inCode):
        try:
            if(TreeCode.objects.get(code=inCode).parent):
                parent = TreeCode.objects.get(code=inCode).parent
                siblingCodes = TreeCode.objects.get(
                    code=parent).children.split(",")
                siblings = TreeCode.objects.filter(code__in=siblingCodes)
                return siblings
            else:
                return TreeCode.objects.filter(code=inCode)
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get_single(self, inCode):
        try:
            selfs = TreeCode.objects.get(code=inCode)
            return selfs
        except ObjectDoesNotExist:
            return None

    def get(self, request, inCode, format=None, **kwargs):
        selfs = self.get_single(inCode)
        if selfs == None:
            return Response({'self': None, 'parent': None, 'siblings': None, 'children': None})
        parent = self.get_single(selfs.parent)
        children = self.get_children(inCode)
        siblings = self.get_siblings(inCode)
        selfSerializer = serializers.TreeCodeSerializer(selfs, many=False)
        parentSerializer = serializers.TreeCodeSerializer(parent, many=False)
        siblingSerializer = serializers.TreeCodeSerializer(siblings, many=True)
        childrenSerializer = serializers.TreeCodeSerializer(
            children, many=True)

        if parent:
            return Response({'self': selfSerializer.data, 'parent': parentSerializer.data, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})
        else:
            return Response({'self': selfSerializer.data, 'parent': None, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})


@permission_classes((permissions.AllowAny,))
class ListMatchingDescriptions(APIView):
    def get_object(self, descSubstring):
        if len(descSubstring) < 3:
            return Code.objects.none()
        return Code.objects.filter(description__icontains=descSubstring).order_by(Length('code').asc())[:15]

    def get(self, request, descSubstring, format=None, **kwargs):
        codes = self.get_object(descSubstring)
        serializer = serializers.CodeSerializer(codes, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListAncestors(APIView):
    def get_object(self, code):
        ancestors = []
        print("Getting ancestors of", code)
        while True:
            try:
                ancestor = TreeCode.objects.get(code=code)
                serializer = serializers.CodeSerializer(ancestor, many=False)
                ancestors.append(serializer)
                code = ancestor.parent
                print("parent:", ancestor.parent)
            except ObjectDoesNotExist:
                return ancestors

    def get(self, request, inCode, format=None, **kwargs):
        ancestors = self.get_object(inCode)
        return Response([ancestor.data for ancestor in ancestors])


@permission_classes((permissions.AllowAny,))
class ListCodeAutosuggestions(APIView):
    def get(self, request, matchString, format=None, **kwargs):
        descMatch = ListMatchingDescriptions()
        codeMatch = ListChildrenOfCode()

        matchesDesc = descMatch.get_object(matchString)
        matchesCode = codeMatch.get_object(matchString)

        serializerDesc = serializers.CodeSerializer(matchesDesc, many=True)
        serializerCode = serializers.CodeSerializer(matchesCode, many=True)
        return Response({"description matches": serializerDesc.data, "code matches": serializerCode.data, "keyword matches": []})


@permission_classes((permissions.AllowAny,))
class CodeUsed(APIView):
    def put(self, request, inCodes, format=None, **kwargs):
        codeList = inCodes.split(",")
        codes = Code.objects.filter(code__in=codeList)
        if len(codes) == len(codeList):
            for code in codes:
                code.times_coded += 1
                code.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)
