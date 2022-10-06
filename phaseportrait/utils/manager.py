import re
import matplotlib
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
        dimension = configuration.get('dimension')
        
        # Parameters
        kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xScale',  'yScale', 'xlabel', 'ylabel', 'color'] + \
            (['zScale', 'zlabel'] if dimension==3 else [])

        for k,v in configuration.items():
            if k in kargs:
                setattr(self.portrait, k, v)
                
        range = configuration.get('Range')
        try:
            if range:
                if dimension == 2:
                    self.portrait.Range = [[range['x_min'],range['x_max']],
                                        [range['y_min'],range['y_max']]]
                if dimension == 3:
                    self.portrait.Range = [[range['x_min'],range['x_max']],
                                        [range['y_min'],range['y_max']],
                                        [range['z_min'], range['z_max']]]
        except TypeError:
            return 1
                
        # Nullclines not implemented in 3d plot
        if (nc:=configuration.get('nullcline')) and dimension != 3:
            self.portrait.add_nullclines(**nc)
        else:
            self.portrait.nullclines = []
            
        if sls:=configuration.get('sliders'):
            for sl_name in sls:
                # If a slider is already created with same name ends are updated and value is changed
                if slider:=self.portrait.sliders.get(sl_name):
                        slider.update_slider_ends(sls[sl_name]["min"], sls[sl_name]["max"])
                        slider.value = configuration["dF_args"][sl_name]
                        slider.slider.set_val(configuration["dF_args"][sl_name])
                
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
        except Exception as e:
            for ax in self.portrait.ax.values():
                ax.cla()
                
        if 'Cobweb' in self.portrait._name_:
            self.portrait.update_dF_args()


        colorbar_check = configuration.get("Colorbar", False)
        self.portrait.colorbar(toggle=colorbar_check)
                
        self.portrait.plot()
            
        self.portrait.fig.tight_layout()
        # self.portrait.fig.subplots_adjust(left=0.2, bottom=0.2, right=1, top=0.9, wspace=0.01, hspace=0.01)
        return 0
        
        
    def equivalent_code(self, configuration):
        """Returns equivalent code of given configuration

        Parameters
        ----------
        configuration : dict
            For more information check api examples

        Returns
        -------
            _description_
        """
        
        match = re.search(r"def\s+(\w+)\(", configuration['dF'])
        function_name = match.group(1)
        dimension = configuration['dimension']

        header = f"""from phaseportrait import *\nimport matplotlib.pyplot as plt"""

        function = f"""\n{configuration['dF']}"""

        portrait = f"""\nphase_diagram = PhasePortrait{dimension}D({function_name}, [[{configuration['Range']['x_min']},{configuration['Range']['x_max']}],[{configuration['Range']['y_min']},{configuration['Range']['y_max']}]]"""
        if dimension == 3:
            portrait = portrait[:-1] + f""",[{configuration['Range']['z_min']},{configuration['Range']['z_max']}]]"""
        
        portrait_kargs = ""
        # kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xlabel', 'ylabel', 'color']
        kargs = ['MeshDim', 'dF_args', 'Density', 'Polar', 'Title', 'xScale',  'yScale', 'xlabel', 'ylabel', 'color'] + \
            (['zScale', 'zlabel'] if dimension==3 else [])
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
        if (nc := configuration.get('nullcline')) and dimension != 3:
            nullcline = f"\nphase_diagram.add_nullclines(precision={nc['precision']}, offset={nc['offset']})"
        
        finisher = '\nphase_diagram.plot()\nplt.show()'

        return header +"\n\t\n"+ function +"\n\t\n"+ portrait +"\n"+ portrait_kargs +"\n\t\n"+ nullcline +"\n\t\n"+ finisher
        
        
    def handle_json(self, message):
        if message["phaseportrait_request"] == '--plot':
            return self.plot_update(message)
        
        if message["phaseportrait_request"] == '--code':
            return self.equivalent_code(message)