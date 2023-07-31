import base64


class StreamlitComponentsHTML:

    @staticmethod
    def get_html_header() -> str:
        '''Create HTML for the header'''
        return '''
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px;">
            <h1 style="margin-left: 0px; font-size: 35px;">ShortGPT</h1>
            <div style="flex-grow: 1; text-align: right;">
                <a href="https://discord.gg/uERx39ru3R" target="_blank" style="text-decoration: none;">
                <button style="margin-right: 10px; padding: 10px 20px; font-size: 16px; color: #fff; background-color: #7289DA; border: none; border-radius: 5px; cursor: pointer;">Join Discord</button>
                </a>
                <a href="https://github.com/RayVentura/ShortGPT" target="_blank" style="text-decoration: none;">
                <button style="padding: 10px 20px; font-size: 16px; color: #fff; background-color: #333; border: none; border-radius: 5px; cursor: pointer;">Add a Star on Github ⭐</button>
                </a>
            </div>
            </div>
        '''

    @staticmethod
    def get_html_error_template() -> str:
        return '''
        <div style='text-align: center; background: #f2dede; color: #a94442; padding: 20px; border-radius: 5px; margin: 10px;'>
          <h2 style='margin: 0;'>ERROR : {error_message}</h2>
          <p style='margin: 10px 0;'>Traceback Info : {stack_trace}</p>
          <p style='margin: 10px 0;'>If the problem persists, don't hesitate to contact our support. We're here to assist you.</p>
          <a href='https://discord.gg/qn2WJaRH' target='_blank' style='background: #a94442; color: #fff; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; text-decoration: none;'>Get Help on Discord</a>
        </div>
        '''

    @staticmethod
    def get_html_video_template(file_url_path, file_name, width="auto", height="auto"):
        """
        Generate an HTML code snippet for embedding and downloading a video.

        Parameters:
        file_url_path (str): The URL or path to the video file.
        file_name (str): The name of the video file.
        width (str, optional): The width of the video. Defaults to "auto".
        height (str, optional): The height of the video. Defaults to "auto".

        Returns:
        str: The generated HTML code snippet.
        """
        html = f'''
            <div style="display: flex; flex-direction: column; align-items: center;">
                <video width="{width}" height="{height}" style="max-height: 100%;" controls>
                    <source src="{file_url_path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <a href="{file_url_path}" download="{file_name}" style="margin-top: 10px;">
                    <button style="font-size: 1em; padding: 10px; border: none; cursor: pointer; color: white; background: #007bff;">Download Video</button>
                </a>
            </div>
        '''
        return html

    @staticmethod
    def add_logo(png_file, st):
        with open(png_file, "rb") as f:
            data = f.read()

        binary_string = base64.b64encode(data).decode()
        background_position = "50% 10%",
        margin_top = "10%",
        image_width = "60%",
        image_height = "192px 192px"
        logo_markup = """
                <style>
                    [data-testid="stSidebarNav"] {
                        background-image: url("data:image/png;base64,%s");
                        background-repeat: no-repeat;
                        background-position: %s;
                        margin-top: %s;
                        background-size: %s %s;
                        background-repeat: no-repeat;
                        padding-top: 120px;
                        background-position: 20px 20px;
                    }

                    [data-testid="stSidebarNav"]::before {
                    content: "SHORT GPT";
                    margin-left: 20px;
                    margin-top: 20px;
                    font-size: 30px;
                    position: relative;
                    top: 100px;
                }
                </style>
                """ % (binary_string, background_position, margin_top, image_width, image_height)

        st.markdown(
            logo_markup,
            unsafe_allow_html=True,
        )
