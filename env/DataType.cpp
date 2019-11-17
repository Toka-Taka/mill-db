#include "DataType.h"
#include <iostream>

using namespace std;

DataType::DataType(Type type) {
	this->type = type;
	this->length = 0;
}

DataType::DataType(DataType::Type type, int length) {
	this->type = type;
	this->length = length;
}

//map<string, DataType::Type> DataType::str_to_type = {
//		{"int", DataType::INT},
//		{"float", DataType::FLOAT},
//		{"double", DataType::DOUBLE},
//		{"char", DataType::CHAR},
//};
//
//
//map<DataType::Type, string> reverse_map(map<string, DataType::Type> str_to_type) {
//	map<DataType::Type, string> reversed;
//	for (auto it = str_to_type.begin(); it != str_to_type.end(); ++it)
//		reversed[it->second] = it->first;
//	return reversed;
//};
//
//map<DataType::Type, string> DataType::type_to_str = {
//		{DataType::INT, "int32_t"},
//		{DataType::FLOAT, "float"},
//		{DataType::DOUBLE, "double"},
//		{DataType::CHAR, "char*"},
//};

//string DataType::convert_type_to_str(DataType::Type type) {
//	auto it = DataType::type_to_str.find(type);
//	if (it == DataType::type_to_str.end())
//		return nullptr;
//	return it->second;
//}

//DataType::Type DataType::convert_str_to_type(string str) {
//	auto it = DataType::str_to_type.find(str);
//	if (it == DataType::str_to_type.end()) {
//		return (DataType::Type) (-1);
//	}
//	return it->second;
//}

DataType::Type DataType::get_typecode() {
	return this->type;
}

int DataType::get_length() {
	return this->length;
}

int DataType::equals(DataType *that) {
	if (this->get_typecode() != that->get_typecode())
		return 0;

	if (this->get_typecode() == DataType::INT)
		return 1;

	if (this->get_typecode() == DataType::DOUBLE)
		return 1;

	if (this->get_typecode() == DataType::FLOAT)
		return 1;

	if (this->get_typecode() == DataType::CHAR)
		return this->get_length() == that->get_length();

	return 0;
}

string DataType::str(string name) {
	if (this->get_typecode() == DataType::INT)
		return "int32_t " + name;

	if (this->get_typecode() == DataType::DOUBLE)
		return "double " + name;

	if (this->get_typecode() == DataType::FLOAT)
		return "float " + name;

	if (this->get_typecode() == DataType::CHAR) {
		string s("char " + name + "[" + to_string(this->get_length()) + "]");
		return s;
	}

	return "";
}

string DataType::str_param_for_select(string name) {
	if (this->get_typecode() == DataType::INT)
		return "int32_t p_" + name;

	if (this->get_typecode() == DataType::DOUBLE)
		return "double p_" + name;

	if (this->get_typecode() == DataType::FLOAT)
		return "float p_" + name;

	if (this->get_typecode() == DataType::CHAR) {
		string s("const char* p_" + name );//+ "[" + to_string(this->get_length()) + "]");
		return s;
	}

	return "";
}

string DataType::str_column_for_select(string name) {
	if (this->get_typecode() == DataType::INT)
		return "int32_t c_" + name;

	if (this->get_typecode() == DataType::DOUBLE)
		return "double c_" + name;

	if (this->get_typecode() == DataType::FLOAT)
		return "float c_" + name;

	if (this->get_typecode() == DataType::CHAR) {
		string s("const char* c_" + name );//[" + to_string(this->get_length()) + "]");
		return s;
	}

	return "";
}


string DataType::str_out(string name) {
	if (this->get_typecode() == DataType::INT)
		return "int32_t " + name;

	if (this->get_typecode() == DataType::DOUBLE)
		return "double " + name;

	if (this->get_typecode() == DataType::FLOAT)
		return "float " + name;

	if (this->get_typecode() == DataType::CHAR) {
		string s("char " + name + "[" + to_string(this->get_length()+1) + "]");
		return s;
	}

	return "";
}

string DataType::signature(string name) {
	if (this->get_typecode() == DataType::INT)
		return "int32_t " + name;

	if (this->get_typecode() == DataType::DOUBLE)
		return "double " + name;

	if (this->get_typecode() == DataType::FLOAT)
		return "float " + name;

	if (this->get_typecode() == DataType::CHAR) {
		return "const char* " + name;
	}

	return "";
}

//string DataType::get_format_specifier() {
//	if (this->get_typecode() == DataType::INT)
//		return "%d";
//
//	if (this->get_typecode() == DataType::DOUBLE)
//		return "%f";
//
//	if (this->get_typecode() == DataType::FLOAT)
//		return "%f";
//
//	if (this->get_typecode() == DataType::CHAR) {
//		return "\\\"%s\\\"";
//	}
//
//	return "";
//}

//string DataType::scan_expr(string column_name) {
//	if (this->get_typecode() == DataType::INT)
//		return "sscanf(token, \"%d\", &(arg->" + column_name + "));";
//
//	if (this->get_typecode() == DataType::DOUBLE)
//		return "sscanf(token, \"%lf\", &(arg->" + column_name + "));";
//
//	if (this->get_typecode() == DataType::FLOAT)
//		return "sscanf(token, \"%f\", &(arg->" + column_name + "));";
//
//	if (this->get_typecode() == DataType::CHAR) {
//		return "memcpy(arg->" + column_name + ", token + sizeof(char), strlen(token)-2);";
//	}
//
//	return "";
//}

//string DataType::init_expr(string column_name) {
//	if (this->get_typecode() == DataType::INT)
//		return "new->" + column_name + " = 0;";
//
//	if (this->get_typecode() == DataType::DOUBLE)
//		return "new->" + column_name + " = 0.0;";
//
//	if (this->get_typecode() == DataType::FLOAT)
//		return "new->" + column_name + " = 0.0;";
//
//	if (this->get_typecode() == DataType::CHAR) {
//		return "memset(new->" + column_name + ", 0, " + to_string(this->get_length()) + ");";
//	}
//
//	return "";
//}

string DataType::select_expr(std::string param, std::string column) {
	if (this->get_typecode() == DataType::INT)
		return "inserted->" + param + " = c_" + column + ";";

	if (this->get_typecode() == DataType::DOUBLE)
		return "inserted->" + param + " = c_" + column + ";";

	if (this->get_typecode() == DataType::FLOAT)
		return "inserted->" + param + " = c_" + column + ";";

	if (this->get_typecode() == DataType::CHAR) {
		return "memcpy(inserted->" + column + ", c_" + param + ", " + to_string(this->get_length()) +
				"); inserted->" + column + "[" + to_string(this->get_length()) + "] = '\\0';";
	}

	return "";
}

string DataType::compare_less_expr(string s1, string col1, string s2, string col2) {
	if (this->get_typecode() == DataType::INT)
		return "(" + s1 + "->" + col1 + " < " + s2 + "->" + col2 + ")";

	if (this->get_typecode() == DataType::DOUBLE)
		return "(" + s1 + "->" + col1 + " < " + s2 + "->" + col2 + ")";

	if (this->get_typecode() == DataType::FLOAT)
		return "(" + s1 + "->" + col1 + " < " + s2 + "->" + col2 + ")";

	if (this->get_typecode() == DataType::CHAR) {
		return "strncmp(" + s1 + "->" + col1 + ", " + s2 + "->" + col2 + ", " + to_string(this->get_length()) + ") < 0";
	}

	return "";
}

string DataType::compare_greater_expr(string s1, string col1, string s2, string col2) {
	if (this->get_typecode() == DataType::INT)
		return "(" + s1 + "->" + col1 + " > " + s2 + "->" + col2 + ")";

	if (this->get_typecode() == DataType::DOUBLE)
		return "(" + s1 + "->" + col1 + " > " + s2 + "->" + col2 + ")";

	if (this->get_typecode() == DataType::FLOAT)
		return "(" + s1 + "->" + col1 + " > " + s2 + "->" + col2 + ")";

	if (this->get_typecode() == DataType::CHAR) {
		return "strncmp(" + s1 + "->" + col1 + ", " + s2 + "->" + col2 + ", " + to_string(this->get_length()) + ") > 0";
	}

	return "";
}
