import copy


def deep_dict_merge(old_dict, new_dict, deep=True):
	if deep:
		old_dict = copy.deepcopy(old_dict)
	else:
		old_dict = old_dict.copy()
	for key, value in new_dict.items():
		if key in old_dict and isinstance(old_dict[key], dict) and isinstance(value, dict):
			old_dict[key] = deep_dict_merge(old_dict[key], value, deep=False)
		else:
			old_dict[key] = value
	return old_dict
