import MainServer
import LocalServer
import numpy as np

favorite = [5, 7, 34, 25, 46, 13, 19, 21, 28, 37]
if __name__ == '__main__':
    main_server = MainServer.MainServer('M4')
    threshold = 30
    local_servers = [LocalServer.LocalServer(f'server_m4_{item}', favorite[item]) for item in range(10)]
    round_number=1000
    summ_E=0
    for _ in range(round_number):  # change for more rounds
        requests_per_server = {}
        for i, server in enumerate(local_servers):
            r_data = server.ask_main_server(MainServer.MainServer.cash_size, threshold)
            requests_per_server[i] = np.random.randint(0, 100, 1, np.uint8)[0]
            main_server.submit_request(i, r_data, server.request_data(r_data))

        results, mood_2 = main_server.process_2()

        for r in results:
            results[r] += [results[r][2] * requests_per_server[r]]
        for r in results:
            for q in main_server.queue:
                if results[r][0] in main_server.queue[q]:
                    results[r] += results[q]

        sorted_results = sorted(results, key=lambda x: results[x][3], reverse=True)
        print('Normal: ', results)
        print('Result: ', sorted_results, 'Mood 2: ', mood_2)
        for cycle, chosen in enumerate(mood_2):
            if cycle > 2:
                break
            # print(f'{cycle} cycle ====> ')

            local_servers[chosen].set_data(results[chosen][0], results[chosen][1])
            for server in local_servers:
                server.upgrade(results[chosen][0], results[chosen][1])
                server.update()

            print(f'Chosen Server by repeat in queue {chosen}: {local_servers[chosen].data} '
                  f'for file {results[chosen][0]} and repeated {mood_2[chosen]} times')
            print(f'Best Chosen Server {sorted_results[cycle]}: {local_servers[sorted_results[cycle]].data} '
                  f'for file {results[sorted_results[cycle]][0]} by {requests_per_server[sorted_results[cycle]]} requests')
            print(f'E: {(-results[chosen][3]+results[sorted_results[cycle]][3])/results[sorted_results[cycle]][3]}')
            summ_E +=(-results[chosen][3]+results[sorted_results[cycle]][3])/results[sorted_results[cycle]][3]
            if(results[chosen][3]<0):
                print("wtf")
        main_server.update()
print ("Avarage of error ", summ_E/round_number)
