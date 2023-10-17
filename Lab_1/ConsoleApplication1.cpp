#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>
#include <queue>

using namespace std;
using namespace chrono;

mutex mtx;
condition_variable cv;
queue<int> waiting_room;

int max_seats = 5;
const int num_customers = 10;
int num_haircuts = 0;

void simulate_barber_work() {
    while (num_haircuts < num_customers) {
        unique_lock<mutex> lock(mtx);

        while (waiting_room.empty()) {
            cout << "Barber is sleeping..." << endl;
            cv.wait(lock);
        }

        int customer = waiting_room.front();

        waiting_room.pop();
        cout << "Barber is cutting hair for client..." << customer << endl;
        num_haircuts++;

        lock.unlock();
        cv.notify_all();
        this_thread::sleep_for(seconds(1));
    }
}

void simulate_customer_action(int id) {
    unique_lock<mutex> lock(mtx);

    if (waiting_room.size() == max_seats) {
        cout << "Client " << id << " leave because waiting room is full" << endl;
        return;
    }

    waiting_room.push(id);
    cout << "Client " << id << " in waiting room" << endl;

    lock.unlock();
    cv.notify_all();

    this_thread::sleep_for(seconds(1));
}

int main() {
    thread barber_thread(simulate_barber_work);
    thread customer_threads[num_customers];

    for (int i = 0; i < num_customers; i++) {
        customer_threads[i] = thread(simulate_customer_action, i);
        this_thread::sleep_for(milliseconds(100));
    }

    for (int i = 0; i < num_customers; i++) {
        customer_threads[i].join();
    }

    barber_thread.join();

    return 0;
}
