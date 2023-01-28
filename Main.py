import dtlpy as dl
from datetime import datetime
import random

dl.login()

dl.projects.list().print()

project = dl.projects.create(project_name='Assignment')

# 2.a
dataset = project.datasets.create(dataset_name='CatsAndDogs')

# 2.b
label1 = dataset.add_label(label_name='class1')
label2 = dataset.add_label(label_name='class2')
label3 = dataset.add_label(label_name='key')

print(dataset.labels)

# 2.c
for i in range(1, 6):
    dataset.items.upload(local_path="/Users/shadaman/Assignment/datasets/file" + str(i) + ".jpeg")

i = 1

randomVal = random.randint(1, 5)

for vals in dataset.items.get_all_items():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    item = dataset.items.get(item_id=vals.id)
    # 2.d
    item.metadata['user'] = dict()
    item.metadata['user']['collectionTime'] = 'collected at' + current_time
    builder = item.annotations.builder()
    if i <= 2:
        # 2.e
        builder.add(annotation_definition=dl.Classification(label='class1'))
        item.annotations.upload(builder)
    else:
        # 2.f
        builder.add(annotation_definition=dl.Classification(label='class2'))
        item.annotations.upload(builder)

    if i is randomVal:
        # 2.g
        builder.add(annotation_definition=dl.Point(x=80, y=80, label='key'))
        item.annotations.upload(builder)
    i += 1
    item.update()

firstFilter = dl.Filters()
firstFilter.add_join(field='label', values='class1')

pointFilter = dl.Filters()
pointFilter.add_join(field='type', values='point')

class1Values = dataset.items.list(filters=firstFilter)
pointAnnotatedValues = dataset.items.list(filters=pointFilter)

# 3
for item in class1Values.all():
    item.print()

print("**********************")
print("**********************")
print("**********************")
print("**********************")
print("**********************")

# 4
for item in pointAnnotatedValues.all():
    item.print()

# recipe = dataset.recipes.create(recipe_name='My Recipe', labels=[label1, label2])
dataset.open_in_web()
