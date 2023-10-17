#include <iostream>
#include <omp.h>
#include <thread>
#include <queue>
#include <chrono>

using namespace std;
using namespace this_thread;
using namespace chrono;

int maxSeats = 5;
int numOfClients = 10;
int numOfHaircuts = 0;

queue<int> waitingRoom;

void SimulateBarberWork()
{
	while (numOfHaircuts < numOfClients)
	{
#pragma omp critical
		if (waitingRoom.empty())
		{
			cout << "Barber is sleeping..." << endl;
		}
		else
		{
			int client = waitingRoom.front();
			waitingRoom.pop();
			cout << "Barber is curring hair for client " + client << endl;
			numOfHaircuts++;
		}

		sleep_for(chrono::seconds(1));
	}
}

void SimulateClientActions(int id)
{
#pragma omp critical
	{
		if (waitingRoom.size() == maxSeats)
		{
			cout << "Client " << id << " leave because waiting room is full" << endl;
			return;
		}

		waitingRoom.push(id);
		cout << "Client " << id << " in waiting room" << endl;
	}

	sleep_for(chrono::seconds(1));
}

int main()
{
#pragma omp parallel sections
	{
#pragma omp section
		{
			SimulateBarberWork();
		}
#pragma omp section
		{
			for (int i = 0; i < numOfClients; i++)
			{
				SimulateClientActions(i);
			}
		}

	}

	return 0;
}