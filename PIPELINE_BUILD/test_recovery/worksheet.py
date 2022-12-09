tweet_index = df['tweet_id']
iteration = 1

while idx < df[0]:
    print("Starting iteration: ", iteration)
    try:
        end_idx, df_w = collect_tweet_df(tweet_index, idx)
        df = pd.concat([df, df_w])
    except Exception as e:
        idx = end_idx
        time.sleep(910)
        iteration += 1
