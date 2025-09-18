DELETE FROM selection_classes;

INSERT INTO selection_classes(class_key) VALUES('course_difficulty');
INSERT INTO selection_class_items(class_id, item_key) VALUES(1, 'course_diff_easy');
INSERT INTO selection_class_items(class_id, item_key) VALUES(1, 'course_diff_mod');
INSERT INTO selection_class_items(class_id, item_key) VALUES(1, 'course_diff_hard');

INSERT INTO selection_classes(class_key) VALUES('course_type');
INSERT INTO selection_class_items(class_id, item_key) VALUES(2, 'course_type_open');
INSERT INTO selection_class_items(class_id, item_key) VALUES(2, 'course_type_mixed');
INSERT INTO selection_class_items(class_id, item_key) VALUES(2, 'course_type_woods');