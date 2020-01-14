from app import mm


class RoleSchema(mm.Schema):
    class Meta:
        fields = ["name"]


class AccountSchema(mm.Schema):
    class Meta:
        fields = ["id", "email", "role"]
    role = mm.Nested(RoleSchema)


class CategorySchema(mm.Schema):
    class Meta:
        fields = ["id", "name"]


class ProductSchema(mm.Schema):
    class Meta:
        fields = ["id", "name", "description", "weight", "price", "added", "seller_id",
                  "category_id"]
    # category = mm.Nested(CategorySchema)
