from pyexpat import model
from django.db.models import fields
from rest_framework import serializers
from ropotApp.models import Area,Branch,ScrappingLogs
from ropotApp.utils.databaseManager import DatabaseManager


class ScrappingLogsS(serializers.ModelSerializer):
    class Meta:
        model = ScrappingLogs
        fields = '__all__'

# region Branches and Areas
class SBranch(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')
    area = serializers.SerializerMethodField('get_area')
    class Meta:
        model = Branch
        fields = ["branch_name","selected","area","count"]

    def get_area(self, branch):
        return branch.area.area_name

    def get_count(self, branch):
            branch_name  = branch.branch_name
            return DatabaseManager().getCountBranch(branch_name)

class SArea(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    class Meta:
        model = Area
        fields = ["area_name","selected","count"]

    def get_count(self, area):
            area_name  = area.area_name
            return DatabaseManager().getCountArea(area_name)

class AreaS(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class BranchS(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
# endregion Branches and Areas

# region Number
class NumbersSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    number = serializers.CharField(read_only=True,max_length=100)
    best = serializers.IntegerField(read_only=True)
    area = serializers.CharField(read_only=True,max_length=50)
    branch = serializers.CharField(read_only=True,max_length=50)
    dateRecord = serializers.CharField(read_only=True,max_length=50)
    version = serializers.CharField(read_only=True,max_length=50)
    best = serializers.IntegerField(read_only=True)
    area_id = serializers.IntegerField(read_only=True)
    branch_id = serializers.IntegerField(read_only=True)
    user_number = serializers.CharField(read_only=True,max_length=50)

    is_valid = serializers.BooleanField(required=False)
    is_deleted = serializers.BooleanField(required=False)
    is_done = serializers.BooleanField(required=False)
    is_new = serializers.BooleanField(required=False)
    is_reserved = serializers.BooleanField(required=False)
    is_available = serializers.BooleanField(required=False)
    is_checked = serializers.BooleanField(required=False)

# endregion Number