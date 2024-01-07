import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import UnivariateSpline


def read_data(file_path):
    """
    Reads the CSV data and returns a DataFrame.
    """
    return pd.read_csv(file_path, usecols=['timeStamp', 'elapsed'])


def calculate_throughput(df, interval='1S', spline_order=5):
    """
    Calculates the throughput (requests per second).
    """
    # Convert timestamp to datetime
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

    # Normalize to relative time (starting from 0)
    df['timeStamp'] -= df['timeStamp'].min()

    # Set timestamp as index
    df.set_index('timeStamp', inplace=True)

    # Resample and count requests per interval
    throughput = df['elapsed'].resample(interval).count()

    throughput = throughput.interpolate(method='spline', order=spline_order)

    return throughput


def calculate_average_response_time(df, interval='1S'):
    """
    Calculates the average response time per interval.
    """
    # Convert timestamp to datetime
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

    # Normalize to relative time (starting from 0)
    df['timeStamp'] -= df['timeStamp'].min()

    # Set timestamp as index
    df.set_index('timeStamp', inplace=True)

    # Resample and calculate average response time per interval
    avg_response_time = df['elapsed'].resample(interval).mean()

    return avg_response_time


def smooth_data(df, spline_order=3):
    """
    Applies spline smoothing to the data.
    """
    # Get x and y values for the spline fit
    x = df.index.astype(np.int64) / 10 ** 9  # Convert to seconds
    y = df.values

    # Fit a spline
    spline = UnivariateSpline(x, y, k=spline_order, s=1)

    # Generate smooth x and y values
    x_smooth = np.linspace(x.min(), x.max(), 300)
    y_smooth = spline(x_smooth)

    return x_smooth, y_smooth


def plot_throughput(data, title='Application Throughput'):
    """
    Plots the throughput data on the same graph with relative time, using spline smoothing.
    """
    plt.figure(figsize=(10, 6))

    for label, df in data.items():
        x_smooth, y_smooth = smooth_data(df)
        plt.plot(x_smooth, y_smooth, label=label)

    plt.title(title)
    plt.xlabel('Relative Time (seconds)')
    plt.ylabel('Requests per Second')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_response_time(data, title='Application Response Time'):
    """
    Plots the average response time data on the same graph with relative time, using spline smoothing.
    """
    plt.figure(figsize=(10, 6))

    for label, df in data.items():
        x_smooth, y_smooth = smooth_data(df)
        plt.plot(x_smooth, y_smooth, label=label)

    plt.title(title)
    plt.xlabel('Relative Time (seconds)')
    plt.ylabel('Average Response Time (ms)')
    plt.legend()
    plt.grid(True)
    plt.show()


def main(file_paths):
    data_throughput = {}
    data_response_time = {}
    for file_path in file_paths:
        label = os.path.basename(file_path)
        df1 = read_data(file_path)
        df2 = read_data(file_path)
        throughput = calculate_throughput(df1)
        response_time = calculate_average_response_time(df2)
        data_throughput[label] = throughput
        data_response_time[label] = response_time

    plot_throughput(data_throughput)
    plot_response_time(data_response_time)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_paths = sys.argv[1:]  # Exclude the script name
        main(file_paths)
    else:
        print("Please provide file paths as command line arguments.")
