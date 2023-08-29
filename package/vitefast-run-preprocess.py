from preprocess import Preprocess


processed_brio = Preprocess("vi", "parent")

# processed_brio.random_dataset(106370)
processed_brio.split_dataset('G:/NLP/brio_v1/source')
# processed_brio.create_source_target("", isAll=True)



# processed_brio.split_directory(self, num_parts, type_document)
# processed_brio.radom_get_num_file("C:/Users/maxco/Desktop/BRIO_RENEW/package/source/original_root/val", "C:/Users/maxco/Desktop/BRIO_RENEW/package/source/split_old_ds/val", 10000)
