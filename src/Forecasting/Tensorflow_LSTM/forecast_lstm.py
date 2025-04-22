import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.dates as mdates
import os


def run_8_1(df: pd.DataFrame, repo_names: list):
    # Make it 2 rows and 4 columns
    fig, axs = plt.subplots(2, 4, figsize=(20, 8))
    # 2D to 1D array (for loop)
    axs = axs.flatten()

    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]

    for idx, repo in enumerate(repo_names):
        repo_df = df[df["repo"] == repo]
        daily_issues = repo_df.groupby(repo_df["created_at"].dt.date).size()
        daily_issues = daily_issues.reindex(pd.date_range(
            daily_issues.index.min(), daily_issues.index.max()), fill_value=0)
        daily_issues.index.name = "date"

        # Normalization
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(daily_issues.values.reshape(-1, 1))

        # Prepare LSTM input
        X, y = [], []
        lookback = 7
        for i in range(lookback, len(scaled)):
            X.append(scaled[i - lookback:i])
            y.append(scaled[i])
        X, y = np.array(X), np.array(y)

        # LSTM model
        model = Sequential()
        model.add(LSTM(64, activation='relu', input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=10, verbose=0)

        # Predict next 7 days
        input_seq = scaled[-lookback:]
        predictions = []
        current_input = input_seq.reshape(1, lookback, 1)

        for _ in range(7):
            pred = model.predict(current_input, verbose=0)[0][0]
            predictions.append(pred)
            current_input = np.append(
                current_input[:, 1:, :], [[[pred]]], axis=1)

        # Inverse transform
        predictions = scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)).flatten()
        predictions = np.where(predictions > 1, np.round(
            predictions).astype(int), predictions)
        max_day = days[np.argmax(predictions)]

        # Draw subplot
        ax = axs[idx]
        ax.bar(days, predictions, color='skyblue')
        ax.set_title(f"{repo}\nMax: {max_day}", fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel("Issues")

    fig.suptitle("Predicted Issues by Weekday per Repo", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # leave space for title

    # Save and close
    output_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "data", "charts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, "8.1.issues_weekday_prediction_all_repos.png")
    plt.savefig(output_path)
    plt.close()


def run_8_2(df: pd.DataFrame, repo_names: list):
    fig, axs = plt.subplots(2, 4, figsize=(20, 8))
    axs = axs.flatten()
    days = ["Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]

    for idx, repo in enumerate(repo_names):
        ax = axs[idx]
        repo_df = df[df["repo"] == repo].dropna(subset=["closed_at"])

        if repo_df.empty:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        daily_closed = repo_df.groupby(repo_df["closed_at"].dt.date).size()
        daily_closed = daily_closed.reindex(pd.date_range(
            daily_closed.index.min(), daily_closed.index.max()), fill_value=0)

        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(daily_closed.values.reshape(-1, 1))

        X, y = [], []
        lookback = 7
        for i in range(lookback, len(scaled)):
            X.append(scaled[i - lookback:i])
            y.append(scaled[i])
        X, y = np.array(X), np.array(y)

        if len(X) == 0:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        model = Sequential()
        model.add(LSTM(64, activation='relu', input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=10, verbose=0)

        # next week
        input_seq = scaled[-lookback:]
        predictions = []
        current_input = input_seq.reshape(1, lookback, 1)

        for _ in range(7):
            pred = model.predict(current_input, verbose=0)[0][0]
            predictions.append(pred)
            current_input = np.append(
                current_input[:, 1:, :], [[[pred]]], axis=1)

        predictions = scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)).flatten()
        predictions = np.where(predictions > 1, np.round(
            predictions).astype(int), predictions)
        max_day = days[np.argmax(predictions)]

        ax.bar(days, predictions, color='lightcoral')
        ax.set_title(f"{repo}\nMax Closed: {max_day}", fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel("Closed Issues")

    fig.suptitle("Predicted Closed Issues by Weekday per Repo", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    output_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "data", "charts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, "8.2.issues_closed_weekday_prediction_all_repos.png")
    plt.savefig(output_path)
    plt.close()


def run_8_3(df: pd.DataFrame, repo_names: list):
    fig, axs = plt.subplots(2, 4, figsize=(20, 8))
    axs = axs.flatten()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for idx, repo in enumerate(repo_names):
        ax = axs[idx]
        repo_df = df[df["repo"] == repo].dropna(subset=["closed_at"])

        if repo_df.empty:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        # group by month
        repo_df["month"] = repo_df["closed_at"].dt.month
        monthly_counts = repo_df.groupby("month").size()
        monthly_counts = monthly_counts.reindex(range(1, 13), fill_value=0)

        # normalize
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(monthly_counts.values.reshape(-1, 1))

        X, y = [], []
        # Use every 3 months to predict
        lookback = 3
        for i in range(lookback, len(scaled)):
            X.append(scaled[i - lookback:i])
            y.append(scaled[i])
        X, y = np.array(X), np.array(y)

        if len(X) == 0:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        model = Sequential()
        model.add(LSTM(64, activation='relu', input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=10, verbose=0)

        # predict next 12 months
        input_seq = scaled[-lookback:]
        predictions = []
        current_input = input_seq.reshape(1, lookback, 1)

        for _ in range(12):
            pred = model.predict(current_input, verbose=0)[0][0]
            predictions.append(pred)
            current_input = np.append(
                current_input[:, 1:, :], [[[pred]]], axis=1)

        predictions = scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)).flatten()
        predictions = np.where(predictions > 1, np.round(
            predictions).astype(int), predictions)
        max_month = months[np.argmax(predictions)]

        ax.bar(months, predictions, color='mediumseagreen')
        ax.set_title(f"{repo}\nMax Closed Month: {max_month}", fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel("Closed Issues")

    fig.suptitle("Predicted Closed Issues by Month per Repo", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    output_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "data", "charts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, "8.3.issues_closed_month_prediction_all_repos.png")
    plt.savefig(output_path)
    plt.close()


def run_8_4(df: pd.DataFrame, repo_names: list):

    fig, axs = plt.subplots(2, 4, figsize=(20, 8))
    axs = axs.flatten()

    for idx, repo in enumerate(repo_names):
        ax = axs[idx]
        repo_df = df[df["repo"] == repo]

        if repo_df.empty:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        daily_created = repo_df.groupby(repo_df["created_at"].dt.date).size()
        daily_created = daily_created.reindex(pd.date_range(
            daily_created.index.min(), daily_created.index.max()), fill_value=0)
        daily_created.index.name = "date"

        # Normalize
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(daily_created.values.reshape(-1, 1))

        X, y = [], []
        lookback = 7
        for i in range(lookback, len(scaled)):
            X.append(scaled[i - lookback:i])
            y.append(scaled[i])
        X, y = np.array(X), np.array(y)

        if len(X) == 0:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        # Train LSTM
        model = Sequential()
        model.add(LSTM(64, activation='relu', input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=10, verbose=0)

        # Predict next 7 days
        input_seq = scaled[-lookback:]
        predictions = []
        current_input = input_seq.reshape(1, lookback, 1)

        for _ in range(7):
            pred = model.predict(current_input, verbose=0)[0][0]
            predictions.append(pred)
            current_input = np.append(
                current_input[:, 1:, :], [[[pred]]], axis=1)

        predictions = scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)).flatten()

        # Plot: real + forecast
        past_dates = daily_created.index[-30:]
        past_values = daily_created.values[-30:]
        future_dates = pd.date_range(
            past_dates[-1] + pd.Timedelta(days=1), periods=7)

        ax.plot(past_dates, past_values, label="Past Created", marker='o')
        ax.plot(future_dates, predictions, label="Forecast",
                linestyle="--", marker='x', color='orange')
        ax.set_title(f"{repo}", fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel("Issues")
        ax.legend()

    fig.suptitle(
        "Forecast of Created Issues per Repo (Next 7 Days)", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    output_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "data", "charts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, "8.4.created_issues_forecast_per_repo.png")
    plt.savefig(output_path)
    plt.close()


def run_8_5(df: pd.DataFrame, repo_names: list):
    fig, axs = plt.subplots(2, 4, figsize=(20, 8))
    axs = axs.flatten()

    for idx, repo in enumerate(repo_names):
        ax = axs[idx]
        repo_df = df[df["repo"] == repo].dropna(subset=["closed_at"])

        if repo_df.empty:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        daily_closed = repo_df.groupby(repo_df["closed_at"].dt.date).size()
        daily_closed = daily_closed.reindex(pd.date_range(
            daily_closed.index.min(), daily_closed.index.max()), fill_value=0)
        daily_closed.index.name = "date"

        # Normalize
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(daily_closed.values.reshape(-1, 1))

        X, y = [], []
        lookback = 7
        for i in range(lookback, len(scaled)):
            X.append(scaled[i - lookback:i])
            y.append(scaled[i])
        X, y = np.array(X), np.array(y)

        if len(X) == 0:
            ax.text(0.5, 0.5, "No enough data in 2 months", fontsize=12,
                    ha='center', va='center', color='gray')
            ax.set_title(f"{repo}", fontsize=10)
            ax.axis("off")
            continue

        model = Sequential()
        model.add(LSTM(64, activation='relu', input_shape=(X.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=10, verbose=0)

        input_seq = scaled[-lookback:]
        predictions = []
        current_input = input_seq.reshape(1, lookback, 1)

        for _ in range(7):
            pred = model.predict(current_input, verbose=0)[0][0]
            predictions.append(pred)
            current_input = np.append(
                current_input[:, 1:, :], [[[pred]]], axis=1)

        predictions = scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)).flatten()

        # Plot
        past_dates = daily_closed.index[-30:]
        past_values = daily_closed.values[-30:]
        future_dates = pd.date_range(
            past_dates[-1] + pd.Timedelta(days=1), periods=7)

        ax.plot(past_dates, past_values, label="Past Closed", marker='o')
        ax.plot(future_dates, predictions, label="Forecast",
                linestyle="--", marker='x', color='orange')
        ax.set_title(f"{repo}", fontsize=10)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel("Issues")
        ax.legend()

    fig.suptitle(
        "Forecast of Closed Issues per Repo (Next 7 Days)", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    output_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "data", "charts"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(
        output_dir, "8.5.closed_issues_forecast_per_repo.png")
    plt.savefig(output_path)
    plt.close()


def main():
    # Get data
    BASE_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", ".."))
    DATA_PATH = os.path.join(BASE_DIR, "Forecasting",
                             "data", "issues_2_months.csv")
    # Read and format
    df = pd.read_csv(DATA_PATH)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["closed_at"] = pd.to_datetime(df["closed_at"])

    repos = [
        "meta-llama/llama3",
        "ollama/ollama",
        "langchain-ai/langchain",
        "langchain-ai/langgraph",
        "microsoft/autogen",
        "openai/openai-cookbook",
        "elastic/elasticsearch",
        "milvus-io/pymilvus"
    ]
    repo_names = df["repo"].unique()

    # # 8.1
    # print("=== 8-1. The day of the week maximum number of issues created ===")
    # run_8_1(df, repo_names)

    # # 8.2
    # print("=== 8-2. The day of the week maximum number of issues closed ===")
    # run_8_2(df, repo_names)

    # print("=== 8-3. The month of the year maximum number of issues closed ===")
    # run_8_3(df, repo_names)

    # print("=== 8-4. Plot the created issues forecast ===")
    # run_8_4(df, repo_names)

    # print("=== 8-5. Plot the closed issues forecast ===")
    # run_8_5(df, repo_names)

    print("=== 8-6. Plot the pulls forecast ===")
    run_8_6(df, repo_names)


if __name__ == "__main__":
    main()
