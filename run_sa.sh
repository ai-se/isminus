[ -d sa_reports ] || mkdir sa_reports
pylint src/whun/whun_helper/input_output.py > sa_reports/input_output_sa.txt
pylint src/whun/whun_helper/item.py > sa_reports/item_sa.txt
pylint src/whun/whun_helper/method.py  > sa_reports/method_sa.txt
pylint src/whun/whun_helper/oracle.py > sa_reports/oracle_sa.txt
pylint src/whun/whun_helper/ranker.py > sa_reports/ranker_sa.txt
pylint src/whun/whun_helper/sat_solver.py > sa_reports/sat_solver_sa.txt
pylint src/whun/whun_helper/search.py > sa_reports/search_sa.txt
pylint src/whun/whun_helper/tree_node.py > sa_reports/tree_node_sa.txt
pylint src/whun/whun.py > sa_reports/whun_sa.txt
