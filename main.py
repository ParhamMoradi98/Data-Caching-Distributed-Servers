import MainServer
import LocalServer
import numpy as np


favorite = [5, 7, 34, 25, 46, 13, 19, 21, 28, 37]
summ_E=0
round_Number=10000
if __name__ == '__main__':
    main_server = MainServer.MainServer('main')
    main_server.cash_size = 10
    threshold = 30
    local_servers = [LocalServer.LocalServer(f'server{item}', favorite[item]) for item in range(10)]

    for _ in range(round_Number):  # change for more rounds
        requests_per_server = {}
        for i, server in enumerate(local_servers):
            r_data = server.ask_main_server(MainServer.MainServer.cash_size, threshold)
            
            requests_per_server[i] = np.random.randint(0, 100, 1, np.uint8)[0]
            main_server.submit_request(i, r_data, server.request_data(r_data))

            server.update()

        results, chosen_key, mood_2 = main_server.process()
        print(results)
        for r in results:
            results[r] += [results[r][2] * requests_per_server[r]]

        best_chosen_key = max(results, key=lambda x: results[x][3])

        local_servers[chosen_key].set_data(results[chosen_key][0], results[chosen_key][1])

        print(f'Chosen Server {chosen_key}: {local_servers[chosen_key].data} for file {results[chosen_key][0]}')
        print(
            f'Chosen Server by repeat in queue {mood_2[0]}: {local_servers[mood_2[0]].data} for file {results[mood_2[0]][0]}'
            f' and repeated {mood_2[1]} times')
        print(f'Best Chosen Server {best_chosen_key}: {local_servers[best_chosen_key].data} '
              f'for file {results[best_chosen_key][0]} by {requests_per_server[best_chosen_key]} requests')
        # print(f'E: {results[chosen_key][3] / results[best_chosen_key][3]}')
        print(f'E: {( results[best_chosen_key][3]-results[chosen_key][3]) / results[best_chosen_key][3]}')
        summ_E +=( results[best_chosen_key][3]-results[chosen_key][3]) / results[best_chosen_key][3]

        main_server.update()
print ("Avarage of error ", summ_E/round_Number)
