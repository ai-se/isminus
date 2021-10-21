[ -d sa_reports ] || mkdir sa_reports
pylint ./whun_helper/input_output.py > sa_reports/input_output_sa.txt
pylint whun_helper/item.py > sa_reports/item_sa.txt
pylint whun_helper/Method. --pyextension-pkg-whitelist=math > sa_reports/Method_sa.txt
pylint whun_helper/oracle.py > sa_reports/oracle_sa.txt
pylint whun_helper/ranker.py > sa_reports/ranker_sa.txt
pylint whun_helper/sat_solver.py > sa_reports/sat_solver_sa.txt
pylint whun_helper/search.py > sa_reports/search_sa.txt
pylint whun_helper/tree_node.py > sa_reports/tree_node_sa.txt
pylint whun.py > sa_reports/whun_sa.txt
