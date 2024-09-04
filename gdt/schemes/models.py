from django.db import models
from enum import Enum

from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

def has_keys(d, keys):
    return set(keys).issubset(d.keys())

def get_nested_value(d, key_string):
    keys = key_string.split('.')
    value = d
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        # Handle the case where the key does not exist
        return None
    
def convert_to_float(value1,value2):
    try:
        compare_value = float(value1)
        compare_to_value = float(value2)
    except ValueError:
        raise ValueError("Unable to convert to float")
    return compare_value,compare_to_value

def convert_to_int(value1,value2):
    try:
        compare_value = int(value1)
        compare_to_value = int(value2)
    except ValueError:
        raise ValueError("Unable to convert to int")
    return compare_value,compare_to_value

def convert_to_array(value1,value2):
    try:
        compare_value=int(value1)
        compare_to_value = len(value2)
    except (TypeError, AttributeError, IndexError, ValueError) as e:
            raise e
    return compare_value,compare_to_value

class CRITERIA_SET_OPERATOR(Enum):
    SATISFY_ALL="SATISFY_ALL"
    EITHER_OR="EITHER_OR"

class CRITERIA_FIELD_TYPES(Enum):
    STRING="STRING"
    DATE="DATE"
    LENGTH="LENGTH"
    OBJECT="OBJECT"
    NUMERIC="NUMERIC"


class SCHEME_CRITERIA_OPERATOR(Enum):
    # Number Operators
    LESS_THAN = '<'
    LESS_THAN_EQUAL="<="
    EQUAL = '='
    GREATER_THAN_EQUAL=">="
    GREATER_THAN = '>'

    #LENGTH Operators
    LENGTH_LESS_THAN = 'l<'
    LENGTH_LESS_THAN_EQUAL="l<="
    LENGTH_EQUAL = 'l='
    LENGTH_GREATER_THAN = 'l>'
    LENGTH_GREATER_THAN_EQUAL="l>="

    #STRING SPECIFIC Operators
    STRING_EQUAL = 's='

class Scheme(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def is_eligible(self,applicant):
        for criteria_set in self.criteria_sets.all():
            if criteria_set.evaluate_set(applicant) == False:
                return False
        return True

class CriteriaSet(models.Model):
    set_operator = models.CharField(
        max_length=11,
        choices=[(status.name, status.name) for status in CRITERIA_SET_OPERATOR],
        default=CRITERIA_SET_OPERATOR.SATISFY_ALL
    )
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    scheme = models.ForeignKey(Scheme,on_delete=models.SET_NULL,null=True,blank=True,related_name="criteria_sets")
    def evaluate_set(self,applicant):
        for child in self.children.all():
            if child.evaluate_set(applicant) == False:
                return False
        criterias = self.criterias.all()
        initial_value = self.set_operator == CRITERIA_SET_OPERATOR.SATISFY_ALL.name
        verdict=initial_value
        for criteria in criterias:     
            if criteria.evaluate_criteria(applicant) is not initial_value:
                verdict=not initial_value
        return verdict

class SchemeCriteria(models.Model):
    criteria_set = models.ForeignKey(CriteriaSet, on_delete=models.CASCADE,related_name="criterias",null=True, blank=True)
    criteria_field = models.CharField(max_length=256)
    criteria_field_type = models.CharField( blank=False,null=False,max_length=28, 
        choices=[(status.name, status.name) for status in CRITERIA_FIELD_TYPES],
        default=CRITERIA_FIELD_TYPES.STRING
        )
    criteria_operator = models.CharField(
        max_length=28, 
        choices=[(status.name, status.name) for status in SCHEME_CRITERIA_OPERATOR],
        default=SCHEME_CRITERIA_OPERATOR.EQUAL
    )
    compare_value = models.CharField(max_length=256)

    def evaluate_criteria(self,value,obj_field=None,obj_operator=None,obj_field_type=None,obj_compare_value=None):
        criteria_field=self.criteria_field if obj_field is None else obj_field
        criteria_operator=self.criteria_operator if obj_operator is None else obj_operator
        criteria_field_type=self.criteria_field_type if obj_field_type is None else obj_field_type
        compare_value = self.compare_value if obj_compare_value is None else obj_compare_value

        #Evaluate string
        if criteria_field_type == CRITERIA_FIELD_TYPES.STRING.name:
            if(criteria_operator == SCHEME_CRITERIA_OPERATOR.STRING_EQUAL.name):
                return compare_value == get_nested_value(value,criteria_field)

        #Evalute Numeric operations
        if criteria_field_type == CRITERIA_FIELD_TYPES.NUMERIC.name:
            try:
                compare_value,compare_to_value = convert_to_float(compare_value,get_nested_value(value,criteria_field))
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.LESS_THAN.name):
                    return compare_to_value<compare_value
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.LESS_THAN_EQUAL.name):
                    return compare_to_value<=compare_value
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.EQUAL.name):
                    return compare_to_value==compare_value
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.GREATER_THAN.name):
                    return compare_to_value>compare_value
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.GREATER_THAN_EQUAL.name):
                    return compare_to_value>=compare_value
            except ValueError:
                print("The value could not be converted to a number.")
                return False

        #Evaluate Array/String
        if criteria_field_type == CRITERIA_FIELD_TYPES.LENGTH.name:
            try:
                compare_value,compare_to_value = convert_to_array(compare_value,get_nested_value(value,criteria_field))
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.LENGTH_LESS_THAN.name):
                    return compare_to_value<compare_value
                if (criteria_operator == SCHEME_CRITERIA_OPERATOR.LENGTH_LESS_THAN_EQUAL.name):
                    return compare_to_value<=compare_value
                if (self.criteria_operator == SCHEME_CRITERIA_OPERATOR.LENGTH_EQUAL.name):
                    return compare_to_value==compare_value
                if (self.criteria_operator == SCHEME_CRITERIA_OPERATOR.LENGTH_GREATER_THAN.name):
                    return compare_to_value>compare_value
                if (self.criteria_operator == SCHEME_CRITERIA_OPERATOR.LENGTH_GREATER_THAN_EQUAL.name):
                    return compare_to_value>=compare_value
            except (TypeError, AttributeError, IndexError, ValueError) as e:
                print("Could not get length")
                return False
        
        # Evaluate Objects
        if self.criteria_field_type == CRITERIA_FIELD_TYPES.OBJECT.name:
            try:    
                compare_json = compare_value.replace("'", "\"")
                object_dict = json.loads(compare_json)

                if has_keys(object_dict,['field','success','operator','type','value']):
                    object_field = object_dict['field']
                    success = int(object_dict['success'])
                    obj_operator = object_dict['operator']
                    field_type=object_dict['type']
                    c_value=object_dict['value']
            
                    object_list = get_nested_value(value,criteria_field)
                    if type(object_list) is not list:
                        print("Invalid list")
                        return False
                    
                    count = 0
                    for obj in object_list:
                        result = self.evaluate_criteria(obj,object_field,obj_operator,field_type,c_value)
                        if(result):
                            count=count+1
                   
                    if criteria_operator == SCHEME_CRITERIA_OPERATOR.EQUAL.name:
                        return success == count
                    if criteria_operator == SCHEME_CRITERIA_OPERATOR.LESS_THAN.name:
                        return success > count
                    if criteria_operator == SCHEME_CRITERIA_OPERATOR.LESS_THAN_EQUAL.name:
                        return success >= count
                    if criteria_operator == SCHEME_CRITERIA_OPERATOR.GREATER_THAN.name:
                        return success < count
                    if criteria_operator == SCHEME_CRITERIA_OPERATOR.GREATER_THAN_EQUAL.name:
                        return success <= count
            except json.JSONDecodeError:
                print("JSON Decode error")
                return False
            except ValueError:
                print("Keys missing in object compare")
                return False

class SchemeNumericBenefit(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE,related_name="num_benefits")
    name = models.CharField(max_length=256)
    amount = models.DecimalField(decimal_places=2,max_digits=12)

class SchemeGeneralBenefit(models.Model):
    scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE,related_name="benefits")
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)

