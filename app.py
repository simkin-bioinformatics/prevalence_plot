from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Dash(__name__)
server = app.server

# read in the prevalence summary file
df = pd.read_csv("prevalence_summaries/DRC_prevalences_with_coords.tsv")

# make a list of all the variants found in the summary file
all_variants = list(df)[4:]
all_variants.sort()
# make a list of all the unique datasets in the Dataset column
datasets = df.Dataset.unique().tolist()
datasets.sort()

# set up the layout for the dash app
app.layout = html.Div(
    [
        # title
        html.Label("Variant"),
        # radio button menu of the variants from the list created above
        dcc.RadioItems(
            value=all_variants[0],
            options=all_variants,
            id="variant-selection",
            inline=True,
        ),
        # tiled map split up by dataset
        dcc.Graph(id="graph-content"),
        # year selector
        dcc.RadioItems(value=datasets[0], options=datasets, id="dataset", inline=True),
        # detail graph 
        dcc.Graph(id="detail-graph"),
    ]
)


# redraw the map whenever the variant-selection radio button item is updated
@app.callback(
    Output("graph-content", "figure"),
    Input("variant-selection", "value"),
)
def update_graph(variant):
    if variant in list(df)[3:]:
        df["prevalence"] = df[variant].str.split(" ").str[0].astype(float)
        max_prevalence = max(df["prevalence"].to_list())
        df["sample_size"] = (
            df[variant].str.split("/").str[1].str.replace(")", "").astype(float)
        )
        filtered_df = df[df["sample_size"] > 0]
        fig = px.scatter_geo(
            filtered_df,
            lat="Latitude",
            lon="Longitude",
            color="prevalence",
            size="sample_size",
            # color_continuous_scale='cividis',
            range_color=(0, max_prevalence),
            scope="africa",
            hover_name="HFname",
            height=800,
            hover_data=["sample_size"],
            # center={"lat": -5.347294315841304, "lon": 34.39018365447818},
            facet_col="Dataset",
        )
        fig.update_traces(
            marker_sizemin=4,
        )
    return fig


@app.callback(
    Output("detail-graph", "figure"),
    Input("dataset", "value"),
    Input("variant-selection", "value"),
)
def make_detail_graph(dataset, variant):
    df = pd.read_csv("prevalence_summaries/DRC_prevalences_with_coords.tsv")
    if variant in list(df)[3:]:
        df["prevalence"] = df[variant].str.split(" ").str[0].astype(float)
        max_prevalence = max(df["prevalence"].to_list())
        df["sample_size"] = (
            df[variant].str.split("/").str[1].str.replace(")", "").astype(float)
        )
        df = df[df["sample_size"] > 0]
        # df = df[df["Dataset"] == int(dataset)]

        fig = px.scatter_map(
            df,
            lat="Latitude",
            lon="Longitude",
            color="prevalence",
            size="sample_size",
            # color_continuous_scale='cividis',
            # range_color=(0, max_prevalence),
            range_color=(0,1),
            zoom=3.8,
            hover_name="province",
            height=600,
            width=600,
            hover_data=["sample_size"],
            center={"lat": -1.6815695315287824, "lon": 22.744896416745945},
        )
    return fig

# print(df)

# if running directly, start it in debug mode
# viewable at localhost:8050
if __name__ == "__main__":
    app.run_server(debug=True)
