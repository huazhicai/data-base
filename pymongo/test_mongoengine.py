from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import connect, Document, EmbeddedDocument, \
    StringField, IntField, FloatField, DateTimeField, ListField, \
    EmbeddedDocumentField

# connect('students')
# connect('students', host='localhost', port=27017)
connect('students', host='mongodb://localhost:27017/students')


class Grade(EmbeddedDocument):
    "students' grade"
    name = StringField(required=True)
    score = FloatField(required=True)


SEX_CHOICES = (
    ('female', 'nv'),
    ('male', 'nan')
)


class Student(Document):
    name = StringField(required=True, max_length=32)
    age = IntField(required=True)
    sex = StringField(required=True, choices=SEX_CHOICES)
    grade = FloatField()
    created_at = DateTimeField(default=datetime.now())
    grades = ListField(EmbeddedDocumentField(Grade))
    address = StringField()
    school = StringField()

    meta = {
        'collection': 'students'
    }


class TestMongoEngine(object):
    def add_one(self):
        chinese = Grade(
                name='chinese',
                score=95
        )
        english = Grade(
                name='english',
                score=89
        )
        stu_obj = Student(
                name='zhangsan',
                age=21,
                sex='male',
                grades=[chinese, english]
        )
        # stu_obj.test = 'OK'
        stu_obj.save()
        return stu_obj

    def get_one(self):
        return Student.objects.first()

    def get_more(self):
        return Student.objects.all()

    def get_one_from_oid(self, oid):
        return Student.objects.filter(id=oid).first()

    def update(self):
        # rest = Student.objects.filter(sex='male').update_one(inc__age=1)
        # return rest
        rest = Student.objects.filter(sex='male').update(inc__age=1)
        return rest

    def delete(self):
        rest = Student.objects.filter(sex='male').first().delete()
        result = Student.objects.filter(sex='male').delete()
        return rest


def main():
    obj = TestMongoEngine()
    # rest = obj.add_one()
    # print(rest.id)

    # rest = obj.get_one()
    # print(rest.id)

    rest = obj.get_more()
    print(type(rest))
    for item in rest:
        print(item.id)

    # rest = obj.get_one_from_oid('593bb8e7fa3ebd091078d40e')
    # print(rest.name)

    # rest = obj.update()
    # print(rest)

    # rest = obj.delete()
    # print(rest)


if __name__ == '__main__':
    main()
