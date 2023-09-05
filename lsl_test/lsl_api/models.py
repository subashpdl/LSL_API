from django.db import models

class LSLScript(models.Model):
    script = models.TextField()
    email = models.EmailField(default='kessel@informatik.uni-mannheim.de')
    share = models.BooleanField(default=True)
    type = models.CharField(max_length=255, default='string')
    execution_id = models.CharField(max_length=255, blank=True, null=True)


    status = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    token = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self):
        return self.script



class Result(models.Model):
    execution_id = models.CharField(max_length=100)
    abstraction_id = models.CharField(max_length=100)
    action_id = models.CharField(max_length=100)
    arena_id = models.CharField(max_length=100)
    sheetid = models.CharField(max_length=100)
    systemid = models.CharField(max_length=100)
    variantid = models.CharField(max_length=100)
    adapterid = models.CharField(max_length=100)
    x = models.CharField(max_length=100)
    y = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    rawvalue = models.CharField(max_length=100)
    valuetype = models.CharField(max_length=100)
    lastmodified = models.CharField(max_length=100)
    executiontime = models.CharField(max_length=100)





    def __str__(self):
        return f"Execution ID: {self.execution_id}, Abstraction ID: {self.abstraction_id}, Action ID: {self.action_id}, Arena ID: {self.arena_id}, Sheet ID: {self.sheetid}, System ID: {self.systemid}, Variant ID: {self.variantid}, Adapter ID: {self.adapterid}, X: {self.x}, Y: {self.y}, Type: {self.type}, Value: {self.value}, Raw Value: {self.rawvalue}, Value Type: {self.valuetype}, Last Modified: {self.lastmodified}, Execution Time: {self.executiontime}"