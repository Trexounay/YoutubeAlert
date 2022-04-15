import os
import srcomapi
from srcomapi import datatypes
from helpers.save import get_save

id = "m362w74m"
api = srcomapi.SpeedrunCom()
run = datatypes.Run(api, data=api.get(f"runs/{id}?r=7"))

print(run.status)

print(os.getcwd())
id = 797183317115142196
n = "cogs.task.streamer"

save = get_save(id, n)
print(save)

save2 = get_save(id, n)
print(save2)

save3 = get_save(id, n)
print(save3)
print(save3.config_file)
