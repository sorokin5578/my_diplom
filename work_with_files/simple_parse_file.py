import csv

def make_csv(path, file_name):
    name = open(path).read().split('\n')
    new_name = []
    cnt=0
    for i in name:
        last_el = len(i) - 1
        if i[last_el] == '0':
            new_name.append({"class": "negative", "title": i[:last_el - 1]})
        if i[last_el] == '1':
            cnt+=1
            if cnt>300:
                continue
            else:
                new_name.append({"class": "positive", "title": i[:last_el - 1]})
    with open(file_name, "w", newline="") as file:
        columns = ["class", "title"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(new_name)

def make_csv_2(negative_path,positive_path,  file_name):
    name1 = open(negative_path).read().split('\n')
    name2 = open(positive_path).read().split('\n')
    new_name = []
    cnt=0
    for i in name1:
        last_el = len(i) - 1
        new_name.append({"class": "negative", "title": i[:last_el - 1]})
    for i in name2:
        last_el = len(i) - 1
        new_name.append({"class": "positive", "title": i[:last_el - 1]})

    with open(file_name, "w", newline="") as file:
        columns = ["class", "title"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(new_name)

# make_csv("C:\\Users\\Illia\\PycharmProjects\\my_diplom\\work_with_files\\imdb_labelled.txt", "new_imdb")
# make_csv("C:\\Users\\Illia\\PycharmProjects\\my_diplom\\work_with_files\\yelp_labelled.txt", "new_yelp")
# make_csv("C:\\Users\\Illia\\PycharmProjects\\my_diplom\\work_with_files\\amazon_cells_labelled.txt", "new_amazon")
# make_csv_2("negative.neg","positive.pos","pos_and_neg")