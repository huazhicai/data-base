from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


class TestMongo(object):

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['blog']

    def add_one(self):
        post = {
            'title': "New Title",
            'content': "blog contents, ...",
            'created_at': datetime.now()
        }
        return self.db.blog.posts.insert_one(post)

    def get_one(self):
        return self.db.blog.posts.find_one()

    def get_more(self):
        return self.db.blog.posts.find({'x': 2})

    def get_one_from_oid(self, oid):
        obj = ObjectId(oid)
        return self.db.blog.posts.find_one({'_id': obj})

    def update(self):
        rest = self.db.blog.update_one({'x': 11}, {'$inc':{'x':10}})
        return rest
        # return self.db.posts.update_many({}, {'$inc': {'x': 10}})

    def delete(self):
        return self.db.blog.posts.delete_one({'x':10})
        # return self.db.blog.posts.delete_many({'x': 12})


def main():
    obj = TestMongo()
    # rest = obj.add_one()
    # print(rest.inserted_id)

    # rest = obj.get_one()
    # print(rest["_id"])

    # rest = obj.get_more()
    # for item in rest:
    #     print(item["_id"])
    #
    # rest = obj.get_one_from_oid('')
    # print(rest)
    #
    # rest = obj.update()
    # print(rest.matched_count)
    # print(rest.modified_count)

    rest = obj.delete()
    print(rest.deleted_count)


if __name__ == '__main__':
    main()
