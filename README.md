# GDT Financial Assistance Scheme System

The goal of this assignment is to build a system that
● Allows the management of a fictitious set of financial assistance schemes.
● Manage accounts of administrators in charge of management of schemes.
● Save and update records of applicants who applied for schemes.
● The system should advise users of schemes that each applicant can apply for.
● The system should also save the outcome of granting of schemes to applicants.

## Description

An in-depth paragraph about your project and overview of use.

### Dependencies

- Python 3.12.5 is my exact version
- asgiref==3.8.1
- Django==5.1
- django-cors-headers==4.4.0
- djangorestframework==3.15.2
- djangorestframework-jsonapi==7.0.2
- djangorestframework-simplejwt==5.3.1
- inflection==0.5.1
- PyJWT==2.9.0
- python-dateutil==2.9.0.post0
- six==1.16.0
- sqlparse==0.5.1

## Getting Started

### Startup using make

- Make sure to install make on Mac `brew install make`
- In the terminal, run `make` in the root folder

### If you don't want to use make

### Installing

- Make sure to create & activate virtual env

```
python -m venv env && env/bin/activate
```

- Install all dependencies using

```
pip install -r gdt/requirements.txt
```

### Executing program

```
python gdt/manage.py makemigrations
python gdt/manage.py migrate
python gdt/manage.py create_admin_user
python gdt/manage.py runserver
```

##Admin Panel
http://localhost:8000/admin

```
Credentials
username = 'admin'
password = 'G0vt3chR0x'
```

##POSTMAN Collection File
GDT-Financial Assitance Schemes.postman_collection.json

## Help

###Database explanation:

####Relationships:

- Applicants have a many-to-many relationship with Family Member. Applicants can have 0 to many family members. Family Member table is used to populate the "household" field when retrieving the applicant

- Schemes have many CriteriaSets. CriteriaSets is in charge of deciding if all SchemeCriterias need to be met(SATISFY_ALL) or only either one(EITHER_ONE) of them are required. CriteriaSets have parents as well to chain multiple CriteriaSets together

For example, you have have a

- CriteriaSet A(value=EITHER_ONE)
- CriteriaSet B that is a child of A where it contains logic that evaluates if the applicant is UNEMPLOYED
- CriteriaSet C is also a child of A where it contains logic that evaluates if the applicant is WIDOWED

so the scheme applies to applicants that are unemployed or widowed

- SchemeCriteria contains the logic for evaluating the applicant.

```
-criteria_set: which criteria_set this SchemeCriteria is part of

-criteria_field: field of interest in the Applicant object

-criteria_field_type: what is the expected type of the value

-criteria_operator: how to evaluate the condition (.e.g. EQUAL,LENGTH_EQUAL,STRING_EQUAL)

-compare_value: the value you compare to
```

For example, in the condition where the applicant needs to be unemployed, the compare_value is "UNEMPLOYED" with the criteria_operator to be STRING_EQUAL

In the event if you use OBJECT as the criteria_field_type, you would have to enter the value for compare_value field in this format

criteria_operator = GREATER_THAN_EQUAL

compare_value = {'field':"education", "success":"1","operator":"STRING_EQUAL","type":"STRING","value":"Primary"}

to evaluate list objects such as household which contains multiple Applicants, we evaluate each member of the household and check if their "education" field is "Primary". "success" field of the JSON will be evaluated along with the criteria_operator(GREATER_THAN_EQUAL), so this means that the applicant has to have at least 1 member in their household to be in primary school.

Any advise for common problems or issues. please contact me at benwubing@gmail.com

## Authors

Contributors names and contact info

ex. Benjamin Wu
ex. [@Benjamin Wu](https://www.linkedin.com/in/benwubing/)

## Version History

- 0.1
  - Initial Release

## License

## Acknowledgments

Inspiration, code snippets, etc.

- [awesome-readme](https://github.com/matiassingers/awesome-readme)
- [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
- [dbader](https://github.com/dbader/readme-template)
- [zenorocha](https://gist.github.com/zenorocha/4526327)
- [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
