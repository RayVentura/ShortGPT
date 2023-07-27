class GradioComponentsHTML:

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
