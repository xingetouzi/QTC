import logging
from rqalpha_mod_optimization.optimizer import SimpleOptimizeApplication
from rqalpha_mod_optimization.parallel import set_parallel_method, ParallelMethod

params = {
    'SHORTPERIOD': range(5,40,5),
}

config = {
    "extra": {
        "log_level": "verbose",
    },
    "base": {
        "start_date": "2015-09-01",
        "end_date": "2017-12-30",
        "accounts": {'stock':1000000},
        "matching_type": "next_bar",
        "benchmark": "000300.XSHG",
        "frequency": "1d",
    }
}

if __name__ == "__main__":
    try:
        set_parallel_method(ParallelMethod.DASK)
        result = SimpleOptimizeApplication(config).open("ROE_MA_Strategy.py").optimize(params)
        print(result.sort_values(by=["sharpe"], ascending=False))
    except Exception as e:
        logging.exception(e)
        print("******POOL TERMINATE*******")