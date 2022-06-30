import re
import matplotlib.pyplot as plt

class Manager:
    def __init__(self, portrait):
        self.portrait = portrait
        
    def plot_update(self, configuration):
        """Updates the plot with the new configuration configuration

        Parameters
        ----------
        configuration : dict
            For more information check api examples

        Returns
        -------
        # TODO:
            _description_
        """

        if range := configuration.get('Range'):
            self.portrait.Range = [[range['x_min'],range['x_max']],
                                    [range['y_min'],range['y_max']]]

        
        # Parameters
        kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xScale',  'yScale', 'xlabel', 'ylabel', 'color']
        for k,v in configuration.items():
            if k in kargs:
                setattr(self.portrait, k, v)
                
        if nc:=configuration.get('nullcline'):
            self.portrait.add_nullclines(**nc)
            
        if sls:=configuration.get('sliders'):
            for sl_name in sls:
                # If a slider is already created with same name ends are updated and value is changed
                if slider:=self.portrait.sliders.get(sl_name):
                        slider.update_slider_ends(sls[sl_name]["min"], sls[sl_name]["max"])
                        slider.value = configuration["dF_args"][sl_name]
                        slider.slider.set_value(configuration["dF_args"][sl_name])
                
                else:
                    self.portrait.add_slider(sl_name, 
                        valinit=configuration["dF_args"][sl_name],
                        valinterval=[sls[sl_name]["min"], sls[sl_name]["max"]],
                        valstep= (sls[sl_name]["max"]-sls[sl_name]["min"])/50
                        )
                    
                    
        if new_dF := configuration.get('dF'):
            self.portrait.dF_args = {}
            try:
                match = re.search(r"def\s+(\w+)\(", new_dF)
                function_name = match.group(1)
                # match = re.search(r"(\s+)def", new_dF)
                # if match is not None:
                #     new_dF = new_dF.replace(match.group(0), "\ndef")
                # del match

                exec(new_dF, globals())
                self.portrait.dF = globals()[function_name]
            except  Exception as e:
                return 1
        
        # Clean axis and replot
        try:
            self.portrait.ax.cla()
        except:
            for ax in self.portrait.ax.values():
                ax.cla()
                
        if 'Cobweb' in self.portrait._name_:
            self.portrait.update_dF_args()

        self.portrait.plot()
        # plt.show()
        return 0
        
        
    def equivalent_code(self, configuration):
        """Returns equivalent code of given configuration

        Parameters
        ----------
        configuration : dict
            For more information check api examples

        Returns
        -------
        # TODO: mensaje de websocket?
            _description_
        """
        
        match = re.search(r"def\s+(\w+)\(", configuration['dF'])
        function_name = match.group(1)

        header = f"""from phaseportrait import *\nimport matplotlib.pyplot as plt"""

        function = f"""\n{configuration['dF']}"""

        portrait = f"""\nphase_diagram = PhasePortrait2D({function_name}, [[{configuration['Range']['x_min']},{configuration['Range']['x_max']}],[{configuration['Range']['y_min']},{configuration['Range']['y_max']}]]"""
        
        portrait_kargs = ""
        kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xlabel', 'ylabel', 'color']
        first = True
        for k in configuration.keys():
            if k in kargs:
                if configuration[k]:
                    if first:
                        portrait += ","
                        first = False
                    if isinstance(configuration[k], str):
                        portrait_kargs += f"\t{k} = '{configuration[k]}',\n"
                    else:
                        portrait_kargs += f"\t{k} = {configuration[k]},\n"
                    
        if first:
            portrait += ')\n'
        else:
            portrait_kargs += ')\n'
        
        nullcline = ''
        if nc := configuration.get('nullcline'):
            nullcline = f"\nphase_diagram.add_nullclines(precision={nc['precision']}, offset={nc['offset']})"
        
        finisher = '\nphase_diagram.plot()\nplt.show()'

        return header +"\n\t\n"+ function +"\n\t\n"+ portrait +"\n"+ portrait_kargs +"\n\t\n"+ nullcline +"\n\t\n"+ finisher
        
        
    def handle_json(self, message):
        if message["phaseportrait_request"] == '--plot':
            return self.plot_update(message)
        
        if message["phaseportrait_request"] == '--code':
            return self.equivalent_code(message)