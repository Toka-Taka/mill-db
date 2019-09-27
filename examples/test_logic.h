#ifndef TEST_LOGIC_H
#define TEST_LOGIC_H

#include <stdint.h>

struct test_logic_handle;

void add_person(int32_t id, const char* name, int32_t age);

struct get_people_either_age_out_data {
	char name[101];
};

struct get_people_either_age_out_service {
	struct test_logic_handle* handle;
	struct get_people_either_age_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_either_age_out {
	struct get_people_either_age_out_service service;
	struct get_people_either_age_out_data data;
};

void get_people_either_age_init(struct get_people_either_age_out* iter, struct test_logic_handle* handle, int32_t age1, int32_t age2);
int get_people_either_age_next(struct get_people_either_age_out* iter);

struct get_people_less_than_id_out_data {
	char name[101];
};

struct get_people_less_than_id_out_service {
	struct test_logic_handle* handle;
	struct get_people_less_than_id_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_less_than_id_out {
	struct get_people_less_than_id_out_service service;
	struct get_people_less_than_id_out_data data;
};

void get_people_less_than_id_init(struct get_people_less_than_id_out* iter, struct test_logic_handle* handle, int32_t id);
int get_people_less_than_id_next(struct get_people_less_than_id_out* iter);

struct get_people_not_equal_age_1_out_data {
	char name[101];
};

struct get_people_not_equal_age_1_out_service {
	struct test_logic_handle* handle;
	struct get_people_not_equal_age_1_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_not_equal_age_1_out {
	struct get_people_not_equal_age_1_out_service service;
	struct get_people_not_equal_age_1_out_data data;
};

void get_people_not_equal_age_1_init(struct get_people_not_equal_age_1_out* iter, struct test_logic_handle* handle, int32_t age);
int get_people_not_equal_age_1_next(struct get_people_not_equal_age_1_out* iter);

struct get_people_not_equal_age_2_out_data {
	char name[101];
};

struct get_people_not_equal_age_2_out_service {
	struct test_logic_handle* handle;
	struct get_people_not_equal_age_2_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_not_equal_age_2_out {
	struct get_people_not_equal_age_2_out_service service;
	struct get_people_not_equal_age_2_out_data data;
};

void get_people_not_equal_age_2_init(struct get_people_not_equal_age_2_out* iter, struct test_logic_handle* handle, int32_t age);
int get_people_not_equal_age_2_next(struct get_people_not_equal_age_2_out* iter);

struct get_people_older_or_same_age_out_data {
	char name[101];
};

struct get_people_older_or_same_age_out_service {
	struct test_logic_handle* handle;
	struct get_people_older_or_same_age_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_older_or_same_age_out {
	struct get_people_older_or_same_age_out_service service;
	struct get_people_older_or_same_age_out_data data;
};

void get_people_older_or_same_age_init(struct get_people_older_or_same_age_out* iter, struct test_logic_handle* handle, int32_t age);
int get_people_older_or_same_age_next(struct get_people_older_or_same_age_out* iter);

struct get_people_older_than_age_out_data {
	char name[101];
};

struct get_people_older_than_age_out_service {
	struct test_logic_handle* handle;
	struct get_people_older_than_age_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_older_than_age_out {
	struct get_people_older_than_age_out_service service;
	struct get_people_older_than_age_out_data data;
};

void get_people_older_than_age_init(struct get_people_older_than_age_out* iter, struct test_logic_handle* handle, int32_t age);
int get_people_older_than_age_next(struct get_people_older_than_age_out* iter);

struct get_people_younger_or_same_age_out_data {
	char name[101];
};

struct get_people_younger_or_same_age_out_service {
	struct test_logic_handle* handle;
	struct get_people_younger_or_same_age_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_younger_or_same_age_out {
	struct get_people_younger_or_same_age_out_service service;
	struct get_people_younger_or_same_age_out_data data;
};

void get_people_younger_or_same_age_init(struct get_people_younger_or_same_age_out* iter, struct test_logic_handle* handle, int32_t age);
int get_people_younger_or_same_age_next(struct get_people_younger_or_same_age_out* iter);

struct get_people_younger_than_age_out_data {
	char name[101];
};

struct get_people_younger_than_age_out_service {
	struct test_logic_handle* handle;
	struct get_people_younger_than_age_out_data* set;
	int size;
	int length;
	int count;
};

struct get_people_younger_than_age_out {
	struct get_people_younger_than_age_out_service service;
	struct get_people_younger_than_age_out_data data;
};

void get_people_younger_than_age_init(struct get_people_younger_than_age_out* iter, struct test_logic_handle* handle, int32_t age);
int get_people_younger_than_age_next(struct get_people_younger_than_age_out* iter);

void test_logic_open_write(const char* filename);
void test_logic_close_write(void);

struct test_logic_handle* test_logic_open_read(const char* filename);
void test_logic_close_read(struct test_logic_handle* handle);

#endif

