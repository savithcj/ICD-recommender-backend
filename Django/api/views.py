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
import random
from django.db.models import Q
from django.db import transaction
from users.models import CustomUser
from django.contrib.auth.hashers import make_password

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        allowedRoles = []
        if request.user.role == "admin":
            return True
        return False

class IsCoder(permissions.BasePermission):
    def has_permission(self, request, view):
        allowedRoles = []
        if request.user.role == "coder":
            return True
        return False

class ListAllRules(APIView):
    """
    Lists all rules
    """
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, format=None, **kwargs):
        queryset = Rule.objects.all()
        serializer = serializers.RulesSerializer(queryset, many=True)
        return Response(serializer.data)


class CreateRule(APIView):
    """Used to manually create a rule from the Admin page"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def post(self, request, format=None, **kwargs):
        # Taking in the body of the request
        body_data = request.data
        # Initializing parameters
        LHSCodes = ''
        RHSCodes = ''
        ageStart = None
        ageEnd = None
        gender = ''

        # Ensuring that the rule has at least one code in the LHS and exactly one in the RHS
        if len(body_data['LHSCodes']) < 1 or len(body_data['RHSCodes']) != 1:
            return HttpResponse(400)

        # Ensuring that the RHS isn't in the LHS
        if(body_data['RHSCodes'][0] in body_data['LHSCodes']):
            return HttpResponse(400)

        # Read and sort LHS codes from json, append to string
        LHSCodesList = list(body_data['LHSCodes'])
        LHSCodesList.sort()
        for counter, code in enumerate(LHSCodesList):
            LHSCodes = LHSCodes + str(code)
            # If the code isn't the last code, add a comma after so the new code can be added
            if counter < len(body_data['LHSCodes']) - 1:
                LHSCodes = LHSCodes + ','

        # Extracting RHS code from a list
        RHSCodesList = list(body_data['RHSCodes'])
        RHSCodes = RHSCodesList[0]

        print(body_data)
        # Taking age start, or setting to 0 if it was not passed
        if 'ageStart' in body_data:
            ageStart = int(body_data['ageStart'])
        else:
            ageStart = 0

        # Taking age end, or setting to 150 if it was not passed
        if 'ageEnd' in body_data:
            ageEnd = int(body_data['ageEnd'])
        else:
            ageEnd = 150

        # If gender is passed, take first character ('M', 'F', or 'O')
        if 'gender' in body_data:
            gender = body_data['gender'][0]
            newRule = Rule.objects.create(
                lhs=LHSCodes, rhs=RHSCodes, min_age=ageStart, max_age=ageEnd, manual=True, gender=gender)
            newRule.save()
        # If gender is not passed, create the rule for both male and female
        else:
            newRuleMale = Rule.objects.create(
                lhs=LHSCodes, rhs=RHSCodes, min_age=ageStart, max_age=ageEnd, manual=True, gender='M')
            newRuleMale.save()
            newRuleFemale = Rule.objects.create(
                lhs=LHSCodes, rhs=RHSCodes, min_age=ageStart, max_age=ageEnd, manual=True, gender='F')
            newRuleFemale.save()

        return HttpResponse(201)


class FlagRuleForReview(APIView):
    """Used to flag a rule for review"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def put(self, request, ruleId, format=None, **kwargs):
        try:
            ruleObj = Rule.objects.get(id=ruleId)
            ruleObj.num_flags += 1  # Increments the number of times the rule has been flagged
            if ruleObj.active is True and ruleObj.review_status == 0:
                ruleObj.review_status = 1  # set to user flagged for admin review status
            ruleObj.save()
            return HttpResponse(200)

        except Exception as e:
            print(e)
            return HttpResponse(400)


class RuleSearch(APIView):
    """Used to search for a rule given LHS and/or RHS codes"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def post(self, request, format=None, **kwargs):
        body_data = request.data
        # Extracting LHS and RHS
        LHSCodesList = list(body_data["LHSCodes"])
        RHSCodesList = list(body_data["RHSCodes"])

        # If there is no codes in the search
        if len(LHSCodesList) < 1 and len(RHSCodesList) < 1:
            return HttpResponse(400)

        rules = Rule.objects.all()

        # Filter the result set using each of the codes from LHS
        # The LHS is equal to the code (only one code in the LHS) OR
        # The LHS ends with the code OR
        # The LHS contains the code and a comma after it
        for code in LHSCodesList:
            rules = rules.filter(Q(lhs=code) | Q(lhs__endswith=code) | Q(lhs__icontains=code+','))

        # Filter the result set using each of the codes from RHS
        # The RHS is equal to the code (only one code in the RHS) OR
        # The RHS ends with the code OR
        # The RHS contains the code and a comma after it
        for code in RHSCodesList:
            rules = rules.filter(Q(rhs=code) | Q(rhs__endswith=code) | Q(rhs__icontains=code+','))

        serializer = serializers.RulesSerializer(rules, many=True)
        return Response(serializer.data)


class ListCodeBlockUsage(APIView):
    """Retrieves the number of times that each code block is used.
    An example of a code block is: A00-A09: Intestinal infectious diseases"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, format=None, **kwargs):
        blocks = CodeBlockUsage.objects.all()
        for block in blocks:
            # Obtaining code and description
            blockObject = TreeCode.objects.get(code=block.block)
            block.description = blockObject.description
            block.parent = blockObject.parent
            parentObject = TreeCode.objects.get(code=block.parent)
            block.parent_description = parentObject.description
        serializer = serializers.CodeBlockUsageSerializer(blocks, many=True)
        return Response(serializer.data)


class SingleCodeDescription(APIView):
    """Returns the description of a single code"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, inCode, format=None, **kwargs):
        try:
            # Gets the code object
            codeObject = Code.objects.get(code=inCode)
        except ObjectDoesNotExist:
            return Response({None})
        serializer = serializers.CodeSerializer(codeObject, many=False)
        return Response(serializer.data)


class ListChildrenOfCode(APIView):
    """Returns the children of a code"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get_object(self, inCode):
        try:
            # Takes the children of the code
            childrenCodes = Code.objects.get(code=inCode).children
            # Turns the children into a list
            childrenCodes = childrenCodes.split(",")
            # Obtains the code objects for each object in the list
            children = Code.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get(self, request, inCode, format=None, **kwargs):
        children = self.get_object(inCode)
        serializer = serializers.CodeSerializer(children, many=True)
        return Response(serializer.data)


class ListRequestedRules(APIView):
    """Returns the rules for the codes entered (entered codes are treated as LHS)"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get_object(self, inCodes, request, active=None):
        try:
            # Sort input codes
            inputCodes = inCodes
            inputCodes = inputCodes.split(",")

            codesToAdd = set()
            for code in inputCodes:
                parent = Code.objects.get(code=code).parent
                codesToAdd.add(parent)
                while True:
                    try:
                        parent = Code.objects.get(code=parent).parent
                        codesToAdd.add(parent)
                    except ObjectDoesNotExist:
                        break

            inputCodes += list(codesToAdd)
            inputCodes.sort()

            # Build combinations of codes
            # max combination in the LHS of 4 codes
            lhs = []
            for i in range(min(len(inputCodes), 4)):
                lhs += list(combinations(inputCodes, i+1))

            # Concatening items in combinations together
            lhs_combinations = []
            for entry in lhs:
                empty = ''
                for i in range(len(entry)):
                    empty += entry[i] + ","
                lhs_combinations.append(empty[:-1])

            # special params
            kwargs = dict()
            kwargs["min_age"] = None
            kwargs["max_age"] = None
            kwargs["gender"] = None
            # get rules
            # sqllite has max query param size of 999
            # weird stuff below to get around max param size. have to get rule ids and then query the rules.
            # direct query will cause overflow of param size
            maxSqlParams = 500
            ruleIds = []
            age_param = request.GET.get('age', None)
            gender_param = request.GET.get('gender', None)
            for i in range(0, len(lhs_combinations), maxSqlParams):
                temp_lhs = lhs_combinations[i:i+maxSqlParams]
                tempRules = Rule.objects.filter(lhs__in=temp_lhs)

                # Excluding rules that aren't for the patient age
                if age_param is not None and age_param.isdigit():
                    age = int(age_param)
                    tempRules = tempRules.filter(min_age__lte=age)
                    tempRules = tempRules.filter(max_age__gte=age)

                # Getting rules for the correct gender
                if gender_param == "Male":
                    tempRules = tempRules.filter(gender='M')
                elif gender_param == "Female":
                    tempRules = tempRules.filter(gender='F')

                for rule in tempRules:
                    # exclude rules with code in RHS that already exist in the LHS
                    if rule.rhs not in inputCodes:
                        ruleIds.append(rule.id)

            # construct a new queryset of rules because the old queryset would cause max param size error
            rules = Rule.objects.filter(id__in=ruleIds)
            if active != None:
                rules = rules.filter(active=active)

            parents = []
            # Adding parts to the rule
            for rule in rules:
                code = Code.objects.get(code=rule.rhs)
                parents.append(code.parent)
                rule.description = code.description
                if rule.oracle == True:
                    rule.conf_factor = 0
                    rule.interact_factor = 0
                    rule.score = 1
                else:
                    N = rule.num_suggested
                    A = rule.num_accepted
                    R = rule.num_rejected
                    S = N/(N+10)  # scales how much confidence vs user interaction affects the score
                    effective_confidence = 0.9*rule.manual + rule.confidence
                    rule.conf_factor = (1-S) * effective_confidence  # confidence based portion of score
                    rule.interact_factor = S * A / (A+R+1)  # interaction based portion of score
                    rule.score = rule.conf_factor + rule.interact_factor
                    # can change conf_factor and interact_factor to non-members of rule later
            # Removing rules which are suggesting a parent if the child is already being suggested
            rulesToRemove = []
            for rule in rules:
                if rule.rhs in parents:
                    rulesToRemove.append(rule)
            rules = list(set(rules)-set(rulesToRemove))
            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, inCodes, format=None, **kwargs):
        rules = self.get_object(inCodes, request)
        serializer = serializers.ExtendedRulesSerializer(rules, many=True)
        return Response(serializer.data)


class ListRequestedRulesActive(APIView):
    """Returns active rules based on the entered codes"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get_object(self, inCodes, request):
        # Creates an instance of the class that returns rules
        listRequested = ListRequestedRules()
        rules = listRequested.get_object(inCodes, request, active=True)
        return rules

    def get(self, request, inCodes, format=None, **kwargs):
        rules = self.get_object(inCodes, request)
        serializer = serializers.ExtendedRulesSerializer(rules, many=True)
        return Response(serializer.data)


class DaggerAsteriskAPI(APIView):
    """Getting dagger/asterisk combinations for any entered codes"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

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



class ListFlaggedRules(APIView):
    """Lists all of the flagged rules"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def get_objects(self):
        try:
            rules = Rule.objects.filter(review_status=1)

            # Append description
            for rule in rules:
                rule.description = "Suggested: "+str(rule.num_suggested) + ", " + \
                    "Accepted: "+str(rule.num_accepted)+", "+"Rejected: "+str(rule.num_rejected)

            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, format=None, **kwargs):
        rules = self.get_objects()
        serializer = serializers.FlaggedRuleSerializer(rules, many=True)
        return Response(serializer.data)


class UpdateFlaggedRule(APIView):
    """Updates flagged rule depending on admin decision"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def put(self, request, ruleIdAndDecision, format=None, **kwargs):
        ruleId, decision = ruleIdAndDecision.split(",")
        try:
            rule = Rule.objects.get(id=ruleId)
            # Rule isn't flagged
            if(rule.review_status == 0):
                return HttpResponse(status=400)
            # Rule has a decision already
            if(rule.review_status == 2 or rule.review_status == 3):
                return HttpResponse(status=400)
            if(decision == "ACCEPT"):  # Change status to accepted
                rule.review_status = 2
            elif(decision == "REJECT"):  # Change status to rejected
                rule.review_status = 3
                rule.active = False
            else:
                return HttpResponse(status=400)

            rule.save()
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)


class Family(APIView):
    """Returns the family of a code"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    # Get the children of the entered code
    def get_children(self, inCode):
        try:
            childrenCodes = TreeCode.objects.get(code=inCode).children
            childrenCodes = childrenCodes.split(",")
            children = TreeCode.objects.filter(code__in=childrenCodes)
            for child in children:
                if child.children:
                    child.hasChildren = True
                else:
                    child.hasChildren = False
            return children
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    # Get the siblings of the entered code
    def get_siblings(self, inCode):
        try:
            if(TreeCode.objects.get(code=inCode).parent):
                parent = TreeCode.objects.get(code=inCode).parent
                siblingCodes = TreeCode.objects.get(
                    code=parent).children.split(",")
                siblings = TreeCode.objects.filter(code__in=siblingCodes)
                for sibling in siblings:
                    if sibling.children:
                        sibling.hasChildren = True
                    else:
                        sibling.hasChildren = False
                return siblings
            else:
                siblings = TreeCode.objects.filter(code=inCode)
                for sibling in siblings:
                    if sibling.children:
                        sibling.hasChildren = True
                    else:
                        sibling.hasChildren = False
                return siblings
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    # Get self of code
    def get_single(self, inCode):
        try:
            selfs = TreeCode.objects.get(code=inCode)
            if selfs.children:
                selfs.hasChildren = True
            else:
                selfs.hasChildren = False
            return selfs
        except ObjectDoesNotExist:
            return None

    # Uses above functions to get family and combine it all
    def get(self, request, inCode, format=None, **kwargs):
        selfs = self.get_single(inCode)
        if selfs == None:
            return Response({'self': None, 'parent': None, 'siblings': None, 'children': None})
        parent = self.get_single(selfs.parent)
        if(parent != None):
            parent.hasChildren = True
            parentSerializer = serializers.TreeCodeSerializer(parent, many=False)
        children = self.get_children(inCode)
        siblings = self.get_siblings(inCode)
        selfSerializer = serializers.TreeCodeSerializer(selfs, many=False)
        siblingSerializer = serializers.TreeCodeSerializer(siblings, many=True)
        childrenSerializer = serializers.TreeCodeSerializer(children, many=True)

        # Sending json
        if parent:
            return Response({'self': selfSerializer.data, 'parent': parentSerializer.data, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})
        else:
            return Response({'self': selfSerializer.data, 'parent': None, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})



class ListMatchingDescriptions(APIView):
    """Used to match text that the user enters in the search box.
    This is so that the user can enter part of the description instead of the code"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get_object(self, searchString):
        # Only check if the length of the entered string is greater than or equal to 3
        if len(searchString) < 3:
            return Code.objects.none()
        # Filters and returns
        searchwords = searchString.lower().split(' ')
        queryset = Code.objects.filter(description__contains=searchwords[0])
        if len(searchwords) > 1:
            for searchword in searchwords[1:]:
                queryset = queryset.filter(description__contains=searchword)
        return queryset.order_by(Length('code').asc())[:15]

    def get(self, request, searchString, format=None, **kwargs):
        codes = self.get_object(searchString)
        serializer = serializers.CodeSerializer(codes, many=True)
        return Response(serializer.data)


class ListMatchingKeywords(APIView):
    """Used to match keywords that the user enters in the search box.
    This is so that the user can enter a keyword instead of the code"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get_object(self, searchString):
        # Only check if the length of the entered string is greater than or equal to 3
        if len(searchString) < 3:
            return Code.objects.none()
        # Filters and returns
        searchwords = searchString.lower().split(' ')
        queryset = Code.objects.filter(keyword_terms__contains=searchwords[0])
        if len(searchwords) > 1:
            for searchword in searchwords[1:]:
                queryset = queryset.filter(keyword_terms__contains=searchword)
        return queryset.order_by(Length('code').asc())[:15]

    def get(self, request, searchString, format=None, **kwargs):
        codes = self.get_object(searchString)
        serializer = serializers.CodeSerializer(codes, many=True)
        return Response(serializer.data)


class ListAncestors(APIView):
    """Lists the ancestors of a code. Used to generate the ancestry chain in the tree"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get_object(self, code):
        ancestors = []
        # Keeps adding ancestors until reaching the top, after which the list is returned
        while True:
            try:
                ancestor = TreeCode.objects.get(code=code)
                serializer = serializers.CodeSerializer(ancestor, many=False)
                ancestors.append(serializer)
                code = ancestor.parent
            except ObjectDoesNotExist:
                return ancestors

    def get(self, request, inCode, format=None, **kwargs):
        ancestors = self.get_object(inCode)
        return Response([ancestor.data for ancestor in ancestors])


class ListCodeAutosuggestions(APIView):
    """Returns codes based upon the text entered"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, searchString, format=None, **kwargs):
        descMatch = ListMatchingDescriptions()
        keywordMatch = ListMatchingKeywords()
        codeMatch = ListChildrenOfCode()

        # Matches descriptions, keywords, or codes
        matchesDesc = descMatch.get_object(searchString)
        matchesKeyword = keywordMatch.get_object(searchString)
        matchesCode = codeMatch.get_object(searchString)

        serializerDesc = serializers.CodeSerializer(matchesDesc, many=True)
        serializerKeyword = serializers.CodeSerializer(matchesKeyword, many=True)
        serializerCode = serializers.CodeSerializer(matchesCode, many=True)
        return Response({"description matches": serializerDesc.data, "code matches": serializerCode.data, "keyword matches": serializerKeyword.data})


class EnterLog(APIView):
    """
    Receives log of user interaction with the system and updates the database.
    """
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def put(self, request, format=None, **kwargs):
        body = request.data
        rules = body['rule_actions']  # Rule id and action
        entered = body['entered']  # List of codes entered
        codes = Code.objects.filter(code__in=entered)  # Removing any potential incorrect codes
        with transaction.atomic():  # To make all of the changes then save them at the same time
            # All rules suggested have num_suggested incremented.
            # Num accepted or rejected incremented based on the action
            for rule in rules:
                ruleObject = Rule.objects.get(id=rule['id'])
                ruleObject.num_suggested += 1
                if rule['action'] == 'A':
                    ruleObject.num_accepted += 1
                elif rule['action'] == 'R':
                    ruleObject.num_rejected += 1
                elif rule['action'] == 'I':
                    pass
                else:
                    return HttpResponse(status=400)
                ruleObject.save()

            # Potentially a false code entered and removed by the query above
            if len(codes) == len(entered):
                for code in codes:
                    code.times_coded += 1
                    code.save()
            else:
                return HttpResponse(status=400)

        return HttpResponse(status=200)


class ChangeRuleStatus(APIView):
    """Used to set a rule to active or inactive"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def patch(self, request, format=None, **kwargs):
        try:
            body_data = request.data
            status = body_data["status"]
            rule_id = body_data["rule_id"]

            # Setting rule status
            rule = Rule.objects.get(id=rule_id)
            rule.active = status
            rule.save()

            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=400)


class InactiveRules(generics.ListAPIView):
    """Returns all rules with inactive status"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    # Gets all rules with active = false
    queryset = Rule.objects.filter(active=False)
    serializer_class = serializers.RulesSerializer


class Stats(APIView):
    """Returns DAD stats to be displayed on the visualization page"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, format=None, **kwargs):
        codes = Code.objects.all()

        sum = 0  # Total number of codes entered
        numUnique = 0  # Number of unique codes entered
        for code in codes:
            sum += code.times_coded_dad
            if code.times_coded_dad > 0:
                numUnique += 1

        # Top 10 common codes
        codes = codes.order_by('-times_coded_dad')[:10]
        topCodes = []
        for code in codes:
            topCodes.append({"code": code.code, "times_coded_dad": code.times_coded_dad,
                             "description": code.description})

        return Response({'totalNumber': sum, 'Top10': topCodes, 'numUnique': numUnique})


class CheckCode(APIView):
    """Checks if a code exists"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, inCode, format=None, **kwargs):
        codes = Code.objects.filter(code=inCode)
        # return true if a code exists
        if codes:
            return Response({'exists': True})
        # return false otherwise
        else:
            return Response({'exists': False})


@permission_classes((permissions.AllowAny,))
class CreateUser(APIView):
"""Is used to create a user when receiving information from the sign-up page"""

    def post(self, request, format=None, **kwargs):
        # Takes in all user info
        body = request.data
        fname = body['fname']
        lname = body['lname']
        email = body['email'].lower()
        password = make_password(body['password'])
        username = body['username'].lower()
        
        # Checks for duplicate username
        try:
            duplicatedUserName = CustomUser.objects.get(username=username)
            return HttpResponse( json.dumps({"message": "Please try a different username."}), status=409)
        except:
            pass
        
        # Checks for duplicate email
        try:
            duplicatedUserEmail = CustomUser.objects.get(email=email)
            return HttpResponse( json.dumps({"message": "Please try a different email address."}), status=409)
        
        # Creates user if no errors from previous checks
        except:
            user = CustomUser.objects.create(first_name=fname, last_name=lname, email=email, password=password, username=username)
            user.save()
            return HttpResponse(json.dumps({"message": "User created."}), status=200)


class ListUnverifiedUsers(APIView):
    """This returns all unverified users for the admin to review"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def get(self, request, format=None, **kwargs):
        # Getting all users with verified = false
        accounts = CustomUser.objects.filter(verified=False)
        serializer = serializers.UserSerializer(accounts, many=True)
        return Response(serializer.data)


class ApproveUser(APIView):
    """This is used to change the verification status of a user to true"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def patch(self, request, format=None, **kwargs):
        try:
            body_data = request.data
            id = body_data["idToApprove"]
            # Verifying user
            user = CustomUser.objects.get(id=id)
            user.verified = True
            user.save()
            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=400)


class RejectUser(APIView):
    """This is used  to remove a user from the system if the admin does not approve their account"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def delete(self, request, idToDelete, format=None, **kwargs):
        try:
            # Deleting the user
            user = CustomUser.objects.get(id=idToDelete)
            user.delete()
            return HttpResponse(status=200)
        except ObjectDoesNotExist:
            return HttpResponse(status=400)


class ValidateToken(APIView, permissions.BasePermission):
    """This is used to validate the token"""
    permission_classes = [permissions.IsAuthenticated,IsAdmin|IsCoder]

    def get(self, request, format=None, **kwargs):
        return HttpResponse(status=200)
