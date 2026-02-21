class DatasetCatalog:
    class DATA_TYPE:
        IMAGES = "images"
        TABULAR = "tabular"
        TEXT = "text"

    class DATASET_KINDS:
        CORPUS = "corpus"
        DATASET = "dataset"

    class DATA_FORMAT:
        FORMATS_IMAGES = ["jpg", "png", "jpeg", "tiff"]
        FORMATS_TABULAR = ["csv", "json", "parquet"]
