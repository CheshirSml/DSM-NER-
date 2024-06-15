import os
import sys
import spacy
import csv
import pandas as pd



model = './model'

def ent_position(doc):
    entity_data = {}

    for ent in doc.ents:
        label = ent.label_
        entity_tokens = [token.i for token in ent]
        adjusted_start = max(0, entity_tokens[0])
        
        merged_segments = []        
        segment_start = None
        segment_end = None

        for i in entity_tokens:
            if not segment_start or i > segment_end+1:
                if segment_start:
                    merged_segments.append((segment_start, segment_end))
                segment_start = i
                segment_end = i
            elif i <= segment_end:
                segment_end += 1

        final_entity_tokens = [adjusted_start] + sorted(merged_segments, key=lambda x: x[0])
        entity_data[label] = final_entity_tokens
    return entity_data

def add_ner_positions(input_csv, output_csv, model):
    
    df = pd.read_csv(input_csv)

    nlp_model = spacy.load(model)

    
    results = []
    for _, row in df.iterrows():
        text = row["processed_text"]
        doc = nlp_model(text)

        if len(doc.ents) == 'О':
            label = {}
        else:
            label = ent_position(doc)

        temp_dict = {k: v for k, v in row.items()}
        temp_dict["labels_position"] = label
        results.append(temp_dict)

    
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)

def visualization_of_entities(model, text):
    nlp = spacy.load(model)
    doc = nlp(text)

    print("\nИменованные сущности и метки:")
    for ent in doc.ents:
        print(ent.text, ent.label_)

    print("\nПозиции сущностей:")
    print(ent_position(doc))
    
    
print("\nПривет! Помогу выявить информацию о скидках в транскрибации текста.")

while True:
    
    print("\nВыбери, что нужно сделать:")
    print("1. Проанализировать текст с помощь NER модели")
    print("2. Добавить список меток и их позиции в тексте в CSV файл")
    print("3. Выход")

    selected_option = int(input())

    if selected_option == 1:
        raw_text = input("\nПожалуйста, введите предложение или абзац для анализа: ")
        model = model
        visualization_of_entities(model, raw_text)
    elif selected_option == 2:
        input_csv = input("\nПредоставить полный путь ввода CSV: ")
        if not os.path.isfile(input_csv):
            raise Exception(f"По данному пути такой файл не найден '{input_csv}'")

        output_csv = input("Введите желаемое имя и формат вывода файла (*.CSV): ")

        if ".csv" not in output_csv:
            output_csv += ".csv"

        add_ner_positions(input_csv, output_csv, model)
        print(f"NER метки успешно записаны в '{output_csv}'")
    elif selected_option == 3:
        print("До свидания! Хорошего дня :)")
        sys.exit(0)
    else:
        print("\nВыбран неверный вариант, попробуйте еще раз!\n")