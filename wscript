import Options, Utils
from os import unlink, symlink, chdir, system
from os.path import exists, lexists

srcdir = "."
blddir = "build"
VERSION = "0.0.1"

def set_options(opt):
  opt.tool_options("compiler_cxx")

def configure(conf):
  conf.check_tool("compiler_cxx")
  conf.check_tool("node_addon")
  conf.check_cfg(package='libgphoto2', args='--cflags --libs', uselib_store='LIBGPHOTO2')
  conf.check_cfg(package='libgphoto2_port', args='--cflags --libs', uselib_store='LIBGPHOTO2PORT')
def build(bld):
  if(exists('src/preview.cc')):
    test = bld.new_task_gen("cxx", "program")
    test.uselib = "LIBGPHOTO2 LIBGPHOTO2PORT"
    test.source = "src/preview.cc"
    test.target = "preview"


  obj = bld.new_task_gen("cxx", "shlib", "node_addon")
  
  obj.cxxflags = ["-D_FILE_OFFSET_BITS=64", "-D_LARGEFILE_SOURCE"]
  obj.uselib = "LIBGPHOTO2 LIBGPHOTO2PORT"
  
  obj.target = "gphoto2"
  obj.source = bld.glob("src/*.cc")
  
  
def shutdown(bld):
  if Options.commands['clean'] and not Options.commands['build']:
    if lexists('gphoto2.node'):
      unlink('gphoto2.node')
  elif Options.commands['build']:
    system('coffee -c test.coffee')
    if exists('build/Release/gphoto2.node') and not lexists('gphoto2.node'):
      symlink('build/Release/gphoto2.node', 'gphoto2.node')
