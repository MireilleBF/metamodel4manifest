class ArtefactCatalog:
    class ACCESS:
        PUBLIC = "public"
        PRIVATE = "private"
        RESTRICTED = "restricted"
        DIRECT_DOWNLOAD = "directDownload"
        ALL = [PUBLIC, PRIVATE, RESTRICTED, DIRECT_DOWNLOAD]
    class CATEGORIES:
        DATA = "data"
        CODE = "code"
        MODEL_WEIGHTS = "model_weights"
        CONFIG = "config"
        PERFORMANCE = "performance"
        VOCABULARY = "vocabulary"
        ALL = [DATA, CODE, MODEL_WEIGHTS, CONFIG, PERFORMANCE]
