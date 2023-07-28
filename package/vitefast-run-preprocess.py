from preprocess import Preprocess


processed_brio = Preprocess("vi", "parent")

# processed_brio.random_dataset(106370)
#processed_brio.split_dataset('C:/Users/maxco/Desktop/BRIO_RENEW/package/source/data_root')
# processed_brio.split_directory(self, num_parts, type_document)
processed_brio.create_source_target("", isAll=True)