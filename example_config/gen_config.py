# This script is meant to simplify generating config files to use 
# with the viewer.  For example, you can add processes, etc, then 
# write out the config to file.  Pass it to the viewer, and it 
# will then use your updated config rather than the default config.
# 

from larcv.config_builder import ConfigBuilder
import json 

def make_config():


    cb = ConfigBuilder()
    # cb.set_parameter([input_file], "InputFiles")
    cb.set_parameter(5, "ProcessDriver", "IOManager", "Verbosity")
    cb.set_parameter(5, "ProcessDriver", "Verbosity")
    cb.set_parameter(5, "Verbosity")

    # Build up the data_keys:
    data_keys = {}
    data_keys['image'] = 'data'

   


    cb.add_preprocess(
        datatype = "sparse2d",
        producer = "dunevoxels",
        process  = "SparseToDense",
        OutputProducer = "dunevoxels"
    )

    cb.add_preprocess(
        datatype = "cluster2d",
        producer = "segment",
        process  = "BBoxFromCluster",
        OutputProducer = "segment",
        MinVoxels = 10
    )

    cb.add_preprocess(
        datatype = "cluster3d",
        producer = "segment",
        process  = "BBoxFromCluster",
        OutputProducer = "segment",
        MinVoxels = 10
    )

    # cb.add_preprocess(
    #     datatype = "sparse2d",
    #     producer = "sbndwire",
    #     process  = "SparseToDense",
    #     OutputProducer = "sbndwire"
    # )
    # cb.add_preprocess(
    #     datatype = "sparse2d",
    #     producer = "sbnd_cosmicseg",
    #     process  = "SparseToDense",
    #     OutputProducer = "sbnd_cosmicseg"
    # )
    # cb.add_preprocess(
    #     datatype = "cluster2d",
    #     producer = "sbndsegmerged",
    #     process  = "BBoxFromCluster",
    #     OutputProducer = "sbndsegmerged"
    # )


    return json.dumps(cb.get_config()["ProcessDriver"])

if __name__ == "__main__":
    cfg = make_config()
    print(cfg)