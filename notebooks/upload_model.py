from roboflow import Roboflow

rf = Roboflow(api_key="y9RCkF9KGh0wVJqkqW1o")
project = rf.workspace().project("hookahs")
model = project.version("5").model

job_id, signed_url, expire_time = model.predict_video(
    "./videos/output_2024-03-16_22-44-07,55.mp4",
    fps=5,
    prediction_type="batch-video",
)

results = model.poll_until_video_results(job_id)

print(results)
